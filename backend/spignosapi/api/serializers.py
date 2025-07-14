"""✅ Pourquoi ?

Convertit les modèles en JSON pour les réponses API.
Relation entre Conversation et Messages."""

from rest_framework import serializers

from .models import Chat, Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "content", "sender", "timestamp"]


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Conversation
        fields = ["id", "title", "user", "created_at", "updated_at", "messages"]


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"  # ou spécifiez les champs que vous voulez exposer
