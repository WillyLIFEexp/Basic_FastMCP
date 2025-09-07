from fastapi import FastAPI

app = FastAPI(title="MCP SQL Helper")

@app.get("/healthz")
def healthz(): return {"ok": True}

@app.get("/mcp/manifest")
def manifest():
    return {
        "name": "mcp-sql-helper",
        "tools": ["generate_sql","optimize_sql","explain_plan","lint_sql"],
        "resources": ["db_connection","schema_snapshot","dialect_profiles"],
        "schema_version": "2025-09"
    }
