from fastapi import FastAPI
from app.routers import chat
from app.config import settings

# Initialisation de l'application FastAPI
app = FastAPI(title="Spignos AI Chat Service",
              description="Service de chat basé sur un modèle LLM",
              version="1.0.0")

# Inclusion des routes
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur Spignos AI Chat Service!"}
