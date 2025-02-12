from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    user_id: str

class ChatResponse(BaseModel):
    response: str
    model: str = "mistralai/Mistral-7B-Instruct"
