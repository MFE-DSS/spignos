from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from datetime import datetime

from .api.models import Conversation, Message
from .api.serializers import MessageSerializer
from .llm.handler import LLMHandler

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from spignosapi.llm.handler import UnifiedLLMHandler

llm_handler = UnifiedLLMHandler(use_openai=True)


# ⚙️ Modèle d'embedding pour la recherche sémantique
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ⚙️ Base de connaissances simulée pour la partie RAG
knowledge_base = [
    "L'IA est utile pour l'automatisation des tâches.",
    "Un modèle LLM peut être utilisé pour la génération de texte.",
    "Le RAG combine un modèle LLM et une base de recherche pour générer des réponses plus précises.",
]

# ⚙️ Indexation FAISS pour recherche vectorielle
knowledge_vectors = np.array(
    [embedding_model.encode(text) for text in knowledge_base], dtype="float32"
)
index = faiss.IndexFlatL2(knowledge_vectors.shape[1])
index.add(knowledge_vectors)


def home_view(request):
    return render(request, "home.html", {"year": datetime.now().year})


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
    🌐 Vue frontend : gère la session utilisateur et affiche la page HTML.
    """
    if not request.session.get("user_id"):
        # 🔐 Création d’un utilisateur anonyme
        username = f"anon_{get_random_string(8)}"
        user = User.objects.create_user(username=username)
        request.session["user_id"] = user.id
    else:
        user = get_object_or_404(User, id=request.session["user_id"])

    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        output = llm_handler.generate(prompt)
        return render(request, "chat.html", {"prompt": prompt, "response": output})

    return render(request, "chat.html")


class ChatAPI(APIView):
    """
    🧠 API REST pour générer une réponse à un prompt utilisateur
    avec une étape RAG (retrieval + génération).
    """

    def post(self, request, conversation_id=None):
        user_input = request.data.get("text", "")

        if not user_input:
            return Response({"error": "Message vide"}, status=status.HTTP_400_BAD_REQUEST)

        # 🎯 Récupération ou création de conversation
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id)
        else:
            conversation = Conversation.objects.create(
                user=request.user
            )  # à adapter si pas d'authentification

        # 🔍 Recherche d'information RAG
        retrieved_info = retrieve_information(user_input)

        # 🧠 Création du prompt enrichi
        prompt = f"Info utile : {retrieved_info}\nQuestion : {user_input}"

        # 💬 Génération de la réponse
        response_text = llm_handler.generate(prompt)

        # 💾 Sauvegarde dans la base
        message = Message.objects.create(
            conversation=conversation, text=user_input, response=response_text
        )

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
