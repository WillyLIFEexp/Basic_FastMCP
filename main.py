from fastapi import FastAPI
from app.database.init_db import init_db
from app.api.v1.auth.routes import router as auth_router

import uvicorn

app = FastAPI(
    title="My FastAPI Tutorial",
    description="A place for me to practice my API.",
    version="1.0.0",
    contact={
        "name": "William",
        "email": "nevergiveupop02@gmail.com",
    },)

init_db()

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

@app.get('/')
def read_root():
    return {"message": "Hello World!!!"}


if __name__ == "__main__":
    uvicorn.run('main:app', port=8000, log_level='info', reload=True)
