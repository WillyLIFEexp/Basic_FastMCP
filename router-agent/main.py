from fastapi import FastAPI

app = FastAPI(title="Router Agent")

@app.get("/healthz")
def healthz(): return {"ok": True}

@app.get("/readyz")
def readyz(): return {"ready": True}

# Stub: in Step 4 we'll actually fetch from MCP servers.
@app.get("/discover")
def discover():
    return {
        "servers": [
            {"name": "mcp-sql-helper", "tools": ["generate_sql","optimize_sql","explain_plan","lint_sql"]},
            {"name": "mcp-english-tutor", "tools": ["rewrite_email","grammar_check","structure"]},
        ]
    }
