from fastapi import FastAPI, HTTPException
import httpx, json
from jsonschema import validate, ValidationError
from pathlib import Path
import os
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv(dotenv_path='.env.example')


MCP_SQL = "http://mcp-sql-helper:8000"
MCP_EN  = "http://mcp-english-tutor:8000"

SCHEMA_DIR = Path(__file__).parent / "schemas"
A2A_TASK_SCHEMA = json.loads((SCHEMA_DIR / "a2a_task.schema.json").read_text(encoding="utf-8"))

OPENAI_MODEL_ROUTER = os.getenv("ROUTER_MODEL", "gpt-4o-mini")

app = FastAPI(title="Router Agent")

@app.get("/healthz")
def healthz(): return {"ok": True}

@app.get("/readyz")
def readyz(): return {"ready": True}

@app.get("/discover")
def discover():
    with httpx.Client(timeout=5.0) as c:
        return {"servers": [
            c.get(f"{MCP_SQL}/mcp/manifest").json(),
            c.get(f"{MCP_EN}/mcp/manifest").json()
        ]}

def validate_a2a_envelope(envelope: dict):
    try:
        validate(instance=envelope, schema=A2A_TASK_SCHEMA)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"A2A schema validation failed: {e.message}")

# Temporary: tiny intent heuristic (5E will expand)
def classify_intent(text: str) -> str:
    lower = text.lower()
    if any(k in lower for k in ["select ", "join ", "index ", "query ", "sql "]):
        return "sql_issue"
    if any(k in lower for k in ["email", "dear", "rewrite", "grammar"]):
        return "english_email"
    return "mixed"

@app.post("/route")
def route(user_input: dict):
    """
    Accepts: { "text": "...", "context": {...} }
    Classifies → builds A2A task → validates → forwards to first hop.
    """
    text = (user_input or {}).get("text") or ""
    if not text.strip():
        raise HTTPException(400, "Missing 'text'")

    intent = classify_intent(text)
    envelope = {
        "type": "task",
        "intent": intent,
        "payload": {"text": text, "context": user_input.get("context", {})},
        "expected": "polished_email" if intent != "sql_issue" else "suggestions",
        "constraints": {"latency_ms": int(os.getenv("TIMEOUT_MS", "30000")), "max_calls": int(os.getenv("MAX_TOOL_CALLS", "3"))}
    }
    validate_a2a_envelope(envelope)

    # First hop
    if intent == "english_email":
        # For now call english tool directly using its own schema default
        with httpx.Client(timeout=15.0) as c:
            payload = {"text": text, "tone": "formal"}  # minimal viable; we’ll map more later
            resp = c.post(f"{MCP_EN}/mcp/call/rewrite_email", json=payload)
            if resp.status_code != 200:
                raise HTTPException(resp.status_code, resp.text)
            return {"intent": intent, "result": resp.json()}
    elif intent == "sql_issue":
        # Stub for now; will wire SQL tool later
        return {"intent": intent, "note": "SQL path stubbed (Step 6)"}
    else:
        # mixed: do English first to keep demo flowing
        with httpx.Client(timeout=15.0) as c:
            payload = {"text": text, "tone": "neutral"}
            resp = c.post(f"{MCP_EN}/mcp/call/rewrite_email", json=payload)
            if resp.status_code != 200:
                raise HTTPException(resp.status_code, resp.text)
            return {"intent": intent, "result": resp.json()}
