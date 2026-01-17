import asyncio
import json
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from ai import ask_gemini, ask_openai, ask_deepseek
from brain import judge_and_route, synthesize_final_answer

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🟢 Client Connected")
    
    chat_history = []
    
    try:
        while True:
            data_raw = await websocket.receive_text()
            data = json.loads(data_raw)
            user_text = data.get("message", "")
            
            print(f"📩 User: {user_text}")

            # 1. JUDGE DECISION
            decision, judge_reply = await judge_and_route(user_text, chat_history)

            final_response = ""
            badge = ""

            if decision == "SIMPLE":
                print("⚡ Mode: Simple")
                final_response = judge_reply
                badge = "⚡ Fast Response"
            else:
                print("🧠 Mode: Complex (Council)")
                await websocket.send_json({"type": "thinking", "msg": "🧠 Convening the Council (Gemini, GPT-4o, DeepSeek)..."})
                
                # Parallel Execution
                r1, r2, r3 = await asyncio.gather(
                    ask_gemini(user_text, chat_history),
                    ask_openai(user_text, chat_history),
                    ask_deepseek(user_text, chat_history)
                )
                
                final_response = await synthesize_final_answer(user_text, r1, r2, r3)
                badge = "🧠 Deep Council"

            # 2. SEND RESPONSE
            await websocket.send_json({
                "type": "response",
                "badge": badge,
                "content": final_response,
                "mode": decision
            })
            
            # 3. UPDATE HISTORY
            chat_history.append({"role": "user", "content": user_text})
            chat_history.append({"role": "assistant", "content": final_response})

    except WebSocketDisconnect:
        print("🔴 Client Disconnected")