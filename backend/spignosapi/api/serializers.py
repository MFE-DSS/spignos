"""✅ Pourquoi ?

Convertit les modèles en JSON pour les réponses API.
Relation entre Conversation et Messages."""

from rest_framework import serializers
from .models import Conversation, Message, Chat


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'content', 'timestamp', 'sender']
        model = Message



class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = "__all__"

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'  # ou spécifiez les champs que vous voulez exposer
