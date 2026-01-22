import os
import asyncio
from dotenv import load_dotenv
from google import genai
from openai import AsyncOpenAI

# Load environment variables
load_dotenv()

# ==========================================
# 🚀 CLIENT SETUP
# ==========================================
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client_openai = AsyncOpenAI(
    api_key=os.getenv("GITHUB_TOKEN_OPENAI"),
    base_url="https://models.github.ai/inference"
)

client_deepseek = AsyncOpenAI(
    api_key=os.getenv("GITHUB_TOKEN_DEEPSEEK"),
    base_url="https://models.github.ai/inference"
)

# ======================================================
# 🛠️ HELPER
# ======================================================
def format_history(user_input, history):
    if not history: return user_input
    context = "Previous Conversation:\n"
    for msg in history:
        role = "User" if msg["role"] == "user" else "AI"
        context += f"- {role}: {msg['content']}\n"
    return context + f"\nCurrent Request: {user_input}"

# ======================================================
# 🤖 WORKERS
# ======================================================
async def ask_gemini(prompt, history=[]):
    try:
        res = await asyncio.to_thread(
            gemini_client.models.generate_content,
            model="gemini-3-flash-preview",
            contents=format_history(prompt, history)
        )
        return res.text
    except Exception as e: return f"[Gemini Error]: {e}"

async def ask_openai(prompt, history=[]):
    try:
        res = await client_openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": format_history(prompt, history)}]
        )
        return res.choices[0].message.content
    except Exception as e: return f"[GPT-4o Error]: {e}"

async def ask_deepseek(prompt, history=[]):
    try:
        # Trying R1 first (Reasoning model)
        res = await client_deepseek.chat.completions.create(
            model="DeepSeek-R1", 
            messages=[{"role": "user", "content": format_history(prompt, history)}]
        )
        return res.choices[0].message.content
    except:
        return "[DeepSeek Error]: Model busy."