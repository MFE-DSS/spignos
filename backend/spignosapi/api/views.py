"""✅ Pourquoi ?

    CreateConversation : Crée une nouvelle conversation.
    ListConversations : Récupère toutes les conversations d’un utilisateur.
    ChatAPI : Ajoute un message et génère une réponse."""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from .middleware import RateLimitedAPIView

class CreateConversation(APIView):
    def post(self, request):
        user = get_object_or_404(User, id=request.data.get("user_id"))
        conversation = Conversation.objects.create(user=user)
        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)

class ListConversations(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        conversations = Conversation.objects.filter(user=user)
        return Response(ConversationSerializer(conversations, many=True).data)

class ChatAPI(APIView):
    def post(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id)
        text = request.data.get("text", "")

        # Simulation de réponse avec un LLM (Mistral, GPT...)
        response_text = f"AI Response: {text[::-1]}"

        message = Message.objects.create(conversation=conversation, text=text, response=response_text)
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)




class ChatAPI(RateLimitedAPIView, APIView):
    def post(self, request):
        message = request.data.get('message', '')
        response_text = f"SPIGNOS AI Response: {message[::-1]}"  # Simulation
        return Response({"response": response_text})
