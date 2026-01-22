# 🧠 Ai-Counsult

A hybrid AI chatbot that intelligently routes questions to the right AI model. Simple questions get instant responses, while complex tasks are solved by a **Council of AI Models** (Gemini, GPT-4o, DeepSeek R1) working together.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-WebSocket-009688?logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- **⚡ Smart Routing** - Simple queries get instant Gemini responses
- **🧠 AI Council** - Complex tasks use 3 AI models in parallel
- **🔄 Real-time** - WebSocket-powered live chat
- **📝 Markdown Support** - Code blocks, formatting, syntax highlighting
- **🌙 Modern UI** - Dark theme with smooth animations

---

## 🏗️ Architecture

```
┌─────────────────┐     WebSocket      ┌─────────────────┐
│     Browser     │ ◄─────────────────► │  FastAPI Server │
│   (Frontend)    │                     │   (server.py)   │
└─────────────────┘                     └────────┬────────┘
                                                 │
                                        ┌────────▼────────┐
                                        │   Brain Layer   │
                                        │   (brain.py)    │
                                        └────────┬────────┘
                                                 │
                    ┌────────────────────────────┼────────────────────────────┐
                    │                            │                            │
           ┌────────▼────────┐          ┌────────▼────────┐          ┌────────▼────────┐
           │     Gemini      │          │     GPT-4o      │          │   DeepSeek R1   │
           └─────────────────┘          └─────────────────┘          └─────────────────┘
```

### How It Works

1. **User sends message** → WebSocket to server
2. **Judge analyzes** → Classifies as SIMPLE or COMPLEX
3. **If SIMPLE** → Gemini responds directly (fast ⚡)
4. **If COMPLEX** → 3 AI models run in parallel, responses are synthesized (🧠)
5. **Final response** → Sent back to user with mode badge

---

## 📁 Project Structure

```
Ai-Counsult/
├── backend/
│   ├── server.py        # FastAPI WebSocket server
│   ├── brain.py         # Judge (router) & Synthesizer
│   ├── ai.py            # AI client configurations
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── index.html       # Main HTML page
│   ├── css/style.css    # Dark theme styling
│   └── js/script.js     # WebSocket client logic
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
cd Ai-Counsult
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the `backend/` folder:

```env
GEMINI_API_KEY=your_gemini_api_key
GITHUB_TOKEN_OPENAI=your_github_models_token
GITHUB_TOKEN_DEEPSEEK=your_github_models_token
```

### 3. Run the Server

```bash
cd backend
uvicorn server:app --reload
```

### 4. Open the Frontend

Open `frontend/index.html` in your browser, or serve it with:

```bash
cd frontend
python -m http.server 5500
```

Then visit: `http://localhost:5500`
