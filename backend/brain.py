import asyncio
from ai import gemini_client, format_history

class Colors:
    CYAN = '\033[96m'; GREEN = '\033[92m'; YELLOW = '\033[93m'; RESET = '\033[0m'

# ======================================================
# ⚖️ THE JUDGE (Smart Router)
# ======================================================
async def judge_and_route(user_input: str, history=[]):
    print(f"{Colors.CYAN}[BRAIN] ⚖️  Judge Analyzing...{Colors.RESET}")
    
    full_prompt = format_history(user_input, history)

    system_instruction = f"""
    You are the Router for an AI System.
    
    INPUT:
    {full_prompt}
    
    TASK: Decide if this needs "Simple" processing or "Complex" reasoning.
    
    CRITERIA FOR 'SIMPLE':
    - Greetings (Hi, Hello).
    - Personal questions (What is your name?).
    - Simple facts (Capital of France?).
    - Short follow-ups to previous simple chats.
    
    CRITERIA FOR 'COMPLEX' (Requires The Council):
    - WRITING CODE (Python, JS, HTML, etc.).
    - Debugging.
    - Mathematical proofs.
    - Creative writing (Poems, Stories).
    - Philosophical debate.
    - Detailed explanations of complex topics.
    
    OUTPUT RULES:
    1. If SIMPLE: Respond directly to the user as a helpful assistant.
    2. If COMPLEX: Output ONLY the string "COMPLEX_MODE". Do not add punctuation.
    """

    try:
        res = await asyncio.to_thread(
            gemini_client.models.generate_content,
            model="gemini-3-flash-preview",
            contents=system_instruction
        )
        response_text = res.text.strip()

        if "COMPLEX_MODE" in response_text:
            return "COMPLEX", None
        else:
            return "SIMPLE", response_text
    except Exception:
        return "COMPLEX", None # Default to smart mode on error

# ======================================================
# 🧪 THE SYNTHESIZER (The Council Leader)
# ======================================================
async def synthesize_final_answer(question, ans_gemini, ans_gpt, ans_deepseek):
    print(f"{Colors.CYAN}[BRAIN] 🧪 Synthesizing 3 Models...{Colors.RESET}")

    prompt = f"""
    You are the Chief Editor of AI Mastermind.
    
    USER QUERY: "{question}"
    
    --- DRAFT 1 (Gemini) ---
    {ans_gemini[:2500]}
    
    --- DRAFT 2 (GPT-4o) ---
    {ans_gpt[:2500]}
    
    --- DRAFT 3 (DeepSeek R1) ---
    {ans_deepseek[:2500]}
    
    GOAL:
    Create ONE perfect response.
    1. If it is code, merge the best logic and provide the cleanest code block.
    2. Remove any internal monologue (like <think> tags).
    3. Be professional and concise.
    """

    try:
        res = await asyncio.to_thread(
            gemini_client.models.generate_content,
            model="gemini-3-flash-preview",
            contents=prompt
        )
        return res.text.strip()
    except Exception as e:
        return f"Synthesis Failed: {e}"