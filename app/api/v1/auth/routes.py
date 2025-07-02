from fastapi import APIRouter, Depends, HTTPException, requests
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token import Token, RefreshTokenRequest
from app.database.session import SessionLocal, get_db
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.crud.user import create_user, authenticate_user, get_user_by_username
from app.core.config import settings
from app.api.deps import get_current_user, require_role
from app.schemas.user import UserResponse
from app.schemas.math_solver import MathRequest
from fastapi import FastAPI, Request
from app.agents.solver_agent import run_math_agent
from fastapi.responses import JSONResponse

import json

router = APIRouter()

def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    user = create_user(db, user_in)
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    payload = decode_token(request.refresh_token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = get_user_by_username(db, payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = create_access_token(data={"sub": user.username})
    new_refresh_token = create_refresh_token(data={"sub": user.username})
    return {"access_token": access_token, "refresh_token": new_refresh_token}

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user = Depends(get_current_user)):
    return current_user

@router.get("/admin", response_model=dict)
def admin_only(current_user = Depends(require_role("admin"))):
    return {"message": f"Welcome, admin {current_user.username}!"}

@router.post("/refresh", response_model=Token)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    payload = decode_token(request.refresh_token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = get_user_by_username(db, payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token(data={"sub": user.username})
    new_refresh_token = create_refresh_token(data={"sub": user.username})  # optional: rotate token

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@router.post("/solve")
async def solve_math(payload: MathRequest):
    question = payload.question.strip()

    if not question:
        return JSONResponse(status_code=400, content={"error": "Missing 'question' field in request"})

    result = await run_math_agent(question)
    return {"result": result}