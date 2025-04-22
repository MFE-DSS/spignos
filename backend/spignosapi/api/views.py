from django.shortcuts import render
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from spignosapi.api.models import Conversation, Message
from spignosapi.api.serializers import MessageSerializer
from spignosapi.llm.handler import LLMHandler, UnifiedLLMHandler
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from drf_spectacular.utils import extend_schema


# Initialisation LLM + Embedding
llm_handler = UnifiedLLMHandler(use_openai=True)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

knowledge_base = [
    "L'IA est utile pour l'automatisation des tâches.",
    "Un modèle LLM peut être utilisé pour la génération de texte.",
    "Le RAG combine un modèle LLM et une base de recherche pour générer des réponses plus précises.",
]
knowledge_vectors = np.array(
    [embedding_model.encode(text) for text in knowledge_base], dtype="float32"
)
index = faiss.IndexFlatL2(knowledge_vectors.shape[1])
index.add(knowledge_vectors)


def retrieve_information(query: str) -> str:
    query_vector = np.array([embedding_model.encode(query)], dtype="float32")
    distances, indices = index.search(query_vector, k=1)
    if distances[0][0] < 1.0:
        return knowledge_base[indices[0][0]]
    return "Pas d'information pertinente trouvée."


@extend_schema(
    request=MessageSerializer,
    responses=MessageSerializer,
    description="Crée un message et génère une réponse via LLM.",
    tags=["Chat"],
)
class ChatAPI(APIView):
    """
    POST /api/chat/ : Génère une réponse avec le LLM (et crée la conversation si nécessaire).
    """

    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.data.get("user_id")
        user_input = request.data.get("text")
        conversation_id = request.data.get("conversation_id")

        if not user_input:
            return Response({"error": "Champ texte manquant"}, status=status.HTTP_400_BAD_REQUEST)

        # Création ou récupération de la conversation
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id)
        elif user_id:
            from django.contrib.auth.models import User

            user = get_object_or_404(User, id=user_id)
            conversation = Conversation.objects.create(user=user)
        else:
            return Response(
                {"error": "user_id ou conversation_id requis"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Enrichissement via RAG
        retrieved_info = retrieve_information(user_input)
        prompt = f"Info utile : {retrieved_info}\nQuestion : {user_input}"
        response_text = llm_handler.generate(prompt)

        # Persistance
        message = Message.objects.create(
            conversation=conversation, text=user_input, response=response_text
        )

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


class ConversationMessagesAPI(APIView):
    """
    GET /api/chat/<conversation_id>/ : Récupère tout l’historique d'une conversation.
    """

    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

    def get(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id)
        messages = conversation.messages.order_by("timestamp")
        return Response(MessageSerializer(messages, many=True).data, status=status.HTTP_200_OK)
