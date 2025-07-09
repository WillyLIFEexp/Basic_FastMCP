from pydantic import BaseModel

class MathRequest(BaseModel):
    question: str