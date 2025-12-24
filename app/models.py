from pydantic import BaseModel

class ResumeRequest(BaseModel):
    text: str

class ResumeResponse(BaseModel):
    score: int
    feedback: list[str]
