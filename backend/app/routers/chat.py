from fastapi import APIRouter
from app.models import ChatRequest, ChatResponse
from transformers import pipeline
from app.config import settings

# Initialisation du router API
router = APIRouter()

# Chargement du modèle Mistral AI depuis Hugging Face
chatbot = pipeline("text-generation", model=settings.MODEL_NAME)

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Gère les requêtes de conversation avec le modèle Mistral AI."""
    response_text = chatbot(request.message, max_length=100, do_sample=True)[0]['generated_text']
    return ChatResponse(response=response_text)
