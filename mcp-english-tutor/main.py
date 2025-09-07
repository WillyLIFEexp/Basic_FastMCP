# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List, Literal

# app = FastAPI(title="MCP English Tutor")

# @app.get("/healthz")
# def healthz(): return {"ok": True}

# @app.get("/mcp/manifest")
# def manifest():
#     return {
#         "name": "mcp-english-tutor",
#         "tools": ["rewrite_email","grammar_check","structure"],
#         "resources": ["style_guides","user_dictionary"],
#         "schema_version": "2025-09"
#     }

# # ---- Tool schemas inline for discovery (mirror your JSON files) ----
# @app.get("/mcp/tools")
# def tools():
#     return {
#         "rewrite_email": {
#             "input_schema": {
#                 "type": "object",
#                 "properties": {
#                     "text": {"type": "string", "minLength": 1},
#                     "tone": {"enum": ["formal","neutral","friendly"]},
#                     "audience": {"type": "string"},
#                     "length": {"enum": ["short","medium","long"]}
#                 },
#                 "required": ["text","tone"],
#                 "additionalProperties": False
#             },
#             "output_schema": {
#                 "type": "object",
#                 "properties": { "revised_text": {"type":"string"} },
#                 "required": ["revised_text"],
#                 "additionalProperties": False
#             }
#         }
#     }

# # ---- Dummy tool: rewrite_email (returns a templated response) ----
# class RewriteEmailIn(BaseModel):
#     text: str
#     tone: Literal["formal","neutral","friendly"]
#     audience: str | None = None
#     length: Literal["short","medium","long"] | None = None

# class RewriteEmailOut(BaseModel):
#     revised_text: str

# @app.post("/mcp/call/rewrite_email", response_model=RewriteEmailOut)
# def call_rewrite_email(inp: RewriteEmailIn):
#     # No LLM yet — just a safe, obvious transformation to prove wiring.
#     prefix = {
#         "formal": "Dear team,",
#         "neutral": "Hello,",
#         "friendly": "Hey there,"
#     }[inp.tone]
#     body = inp.text.strip()
#     signoff = "Best regards," if inp.tone != "friendly" else "Cheers,"
#     revised = f"{prefix}\n\n{body}\n\n{signoff}\nMCP English Tutor"
#     return {"revised_text": revised}


from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
import json
from pathlib import Path
import os
from openai import OpenAI
from fastapi import HTTPException
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv(dotenv_path='.env.example')

app = FastAPI(title="MCP English Tutor")

SCHEMA_DIR = Path(__file__).parent / "schemas"
REWRITE_SCHEMA = json.loads((SCHEMA_DIR / "tool_rewrite_email.schema.json").read_text(encoding="utf-8"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ENGLISH_MODEL = os.getenv("ENGLISH_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = """You are an assistant that rewrites business emails.
- Preserve factual content.
- Improve clarity, tone, and grammar.
- Do NOT invent data.
- Respect the specified tone: formal | neutral | friendly.
- If audience is given, tailor greeting and register appropriately.
- Keep the message concise; avoid flowery language.
Return ONLY the rewritten email text.
"""

@app.get("/healthz")
def healthz(): return {"ok": True}

@app.get("/mcp/manifest")
def manifest():
    return {
        "name": "mcp-english-tutor",
        "tools": ["rewrite_email","grammar_check","structure"],
        "resources": ["style_guides","user_dictionary"],
        "schema_version": "2025-09"
    }

@app.get("/mcp/tools")
def tools():
    # Serve the exact schema file so router and tests share the same truth.
    return {"rewrite_email": REWRITE_SCHEMA}

# Pydantic I/O models to keep FastAPI happy (mirror the schema)
class RewriteEmailIn(BaseModel):
    text: str
    tone: Literal["formal","neutral","friendly"]
    audience: str | None = None
    length: Literal["short","medium","long"] | None = None

class RewriteEmailOut(BaseModel):
    revised_text: str

@app.post("/mcp/call/rewrite_email", response_model=RewriteEmailOut)
def call_rewrite_email(inp: RewriteEmailIn):
    if len(inp.text) > 6000:
        raise HTTPException(400, "Input too long")
    tone = inp.tone
    instructions = []
    if inp.audience: instructions.append(f"Audience: {inp.audience}")
    if inp.length:   instructions.append(f"Target length: {inp.length}")
    instructions.append(f"Tone: {tone}")

    prompt = (
        "Rewrite the following message as a polished business email.\n\n"
        + "\n".join(instructions) + "\n\n"
        + "Original message:\n" + inp.text.strip()
    )

    try:
        resp = client.chat.completions.create(
            model=ENGLISH_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=600
        )
        out = resp.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(500, f"LLM error: {e}")

    return {"revised_text": out}