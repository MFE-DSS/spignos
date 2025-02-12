

from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import SessionLocal, ChatMessage


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    response_text = chatbot(request.message, max_length=100, do_sample=True)[0]['generated_text']

    # Enregistrer la conversation dans la DB
    new_chat = ChatMessage(user_id=request.user_id, message=request.message, response=response_text)
    db.add(new_chat)
    db.commit()

    return ChatResponse(response=response_text)
