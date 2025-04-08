from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .api.models import Conversation, Message
from .api.serializers import MessageSerializer
from .llm.handler import LLMHandler

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ⚙️ Chargement unique du modèle LLM (handler local)
llm_handler = LLMHandler()

# ⚙️ Modèle d'embedding pour la recherche sémantique
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ⚙️ Base de connaissances simulée pour la partie RAG
knowledge_base = [
    "L'IA est utile pour l'automatisation des tâches.",
    "Un modèle LLM peut être utilisé pour la génération de texte.",
    "Le RAG combine un modèle LLM et une base de recherche pour générer des réponses plus précises."
]

# ⚙️ Indexation FAISS pour recherche vectorielle
knowledge_vectors = np.array([embedding_model.encode(text) for text in knowledge_base], dtype="float32")
index = faiss.IndexFlatL2(knowledge_vectors.shape[1])
index.add(knowledge_vectors)


def retrieve_information(query: str) -> str:
    """
    🔍 Recherche d'informations pertinentes via FAISS dans la base simulée.
    """
    query_vector = np.array([embedding_model.encode(query)], dtype="float32")
    distances, indices = index.search(query_vector, k=1)

    if distances[0][0] < 1.0:  # Seuil configurable
        return knowledge_base[indices[0][0]]

    return "Pas d'information pertinente trouvée."


@csrf_exempt
def chat_page(request):
    """
    🌐 Vue front pour la page de chat (HTML).
    """
    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        output = llm_handler.generate(prompt)
        return render(request, "chat.html", {"prompt": prompt, "response": output})

    return render(request, "chat.html")


class ChatAPI(APIView):
    """
    🧠 API REST pour générer une réponse
