from django.urls import path
from .views import ChatAPI, ConversationMessagesAPI

urlpatterns = [
    path("chat/", ChatAPI.as_view(), name="chat_create_or_reply"),
    path("chat/<int:conversation_id>/", ConversationMessagesAPI.as_view(), name="chat_history"),
]
