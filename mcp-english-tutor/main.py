from fastapi import FastAPI

app = FastAPI(title="MCP English Tutor")

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
