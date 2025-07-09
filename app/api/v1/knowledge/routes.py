from fastapi import APIRouter
from app.agents.router_agent import run_router
from app.models.vocab import QueryRequest

router = APIRouter()


@router.post("/ask_vocab")
async def ask_router(request: QueryRequest):
    response = run_router(request.query)
    return {"response": response}