from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from config import client, MODEL
from schemas import ChatRequest
from prompts import PERSONAS
from classifier import predict_persona

app = FastAPI(title="AI Code Assistant", version="1.0.0")

# allow requests from Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ─── Chat ────────────────────────────────────────────

@app.post("/chat")
async def chat(request: ChatRequest):
    # Use Decision Tree to auto-detect persona if not provided
    persona = request.persona
    if not persona or persona not in PERSONAS:
        # Get the last user message
        if request.messages:
            last_message = request.messages[-1].content
            persona = predict_persona(last_message)
        else:
            persona = "assistant"  # Default fallback
    
    if persona not in PERSONAS:
        raise HTTPException(status_code=400, detail="Invalid persona")

    messages = [
        {"role": "system", "content": PERSONAS[persona]},
        *[{"role": m.role, "content": m.content} for m in request.messages]
    ]

    if request.stream:
        def stream():
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=True
            )
            for chunk in response:
                token = chunk.choices[0].delta.content
                if token:
                    yield token
        return StreamingResponse(stream(), media_type="text/plain")
    else:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=False
        )
        return {"content": response.choices[0].message.content}

# ─── Personas ────────────────────────────────────────
@app.get("/personas")
def list_personas():
    return [
        {"key": "assistant", "label": "Assistant", "icon": "🤖"},
        {"key": "reviewer",  "label": "Reviewer",  "icon": "🔍"},
        {"key": "debugger",  "label": "Debugger",  "icon": "🐛"},
        {"key": "explainer", "label": "Explainer", "icon": "📖"},
    ]

# ─── Health Check ────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}