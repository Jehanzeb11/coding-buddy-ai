from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from config import client, MODEL
from schemas import ChatRequest
from prompts import PERSONAS

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
    if request.persona not in PERSONAS:
        raise HTTPException(status_code=400, detail="Invalid persona")

    def stream():
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": PERSONAS[request.persona]},
                *[{"role": m.role, "content": m.content} for m in request.messages]
            ],
            stream=True
        )
        for chunk in response:
            token = chunk.choices[0].delta.content
            if token:
                yield token

    return StreamingResponse(stream(), media_type="text/plain")

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