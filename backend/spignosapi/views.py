from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from backend.spignosapi.api.models import Conversation, Message

from backend.spignosapi.api.serializers import MessageSerializer  # ✅ Correction de l'importation

from transformers import pipeline
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from django.shortcuts import render


# 🔹 Charger un modèle de génération de texte (LLM)
llm_pipeline = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.1")

# 🔹 Charger un modèle d'encodage pour la recherche (RAG)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# 🔹 Simuler une base de connaissances (pour RAG)
knowledge_base = [
    "L'IA est utile pour l'automatisation des tâches.",
    "Un modèle LLM peut être utilisé pour la génération de texte.",
    "Le RAG combine un modèle LLM et une base de recherche pour générer des réponses plus précises."
]

# 🔹 Indexer la base de connaissances avec FAISS (accélération des recherches)
knowledge_vectors = np.array([embedding_model.encode(text) for text in knowledge_base], dtype="float32")
index = faiss.IndexFlatL2(knowledge_vectors.shape[1])
index.add(knowledge_vectors)


def chat_page(request):
    return render(request, 'chat.html')


def retrieve_information(query):
    """
    Recherche les informations les plus pertinentes à partir de la base de connaissances.
    """
    query_vector = np.array([embedding_model.encode(query)], dtype="float32")
    distances, indices = index.search(query_vector, k=1)

    if distances[0][0] < 1.0:  # Seuil d'acceptation pour considérer l'info comme pertinente
        return knowledge_base[indices[0][0]]
    return "Pas d'information pertinente trouvée."


class ChatAPI(APIView):
    """
    API permettant de générer une réponse en utilisant un LLM avec une couche RAG.
    """

    def post(self, request, conversation_id=None):
        user_input = request.data.get("text", "")

        if not user_input:
            return Response({"error": "Message vide"}, status=status.HTTP_400_BAD_REQUEST)

        # 🔹 Vérifier si la conversation existe ou en créer une
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id)
        else:
            conversation = Conversation.objects.create(user=request.user)  # À adapter avec l'authentification

        # 🔹 Étape RAG : Recherche d'informations pertinentes
        retrieved_info = retrieve_information(user_input)

        # 🔹 Construire le prompt pour le modèle LLM
        prompt = f"Info utile : {retrieved_info}\nQuestion : {user_input}"

        # 🔹 Générer la réponse avec le LLM
        response = llm_pipeline(prompt, max_length=200, do_sample=True)
        response_text = response[0]["generated_text"]

        # 🔹 Enregistrer la conversation
        message = Message.objects.create(conversation=conversation, text=user_input, response=response_text)

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
