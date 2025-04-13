""" Pourquoi ?

    Conversation : Un utilisateur peut avoir plusieurs conversations.
    Message : Chaque conversation a plusieurs messages."""
from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'api'  # Ajoute ceci pour préciser l'application


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()
    response = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'api'  # Ajoute ceci pour préciser l'application
