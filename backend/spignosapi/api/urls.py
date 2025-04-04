"""✅ Pourquoi ?

    Les URLs suivent une convention REST propre."""

from django.urls import path, include
from .views import CreateConversation, ListConversations, ChatAPI


urlpatterns = [
    path('conversation/create/', CreateConversation.as_view(), name="create_conversation"),
    path('conversations/<int:user_id>/', ListConversations.as_view(), name="list_conversations"),
    path('chat/<int:conversation_id>/', ChatAPI.as_view(), name="chat_api"),
    path('api/auth/', include('spignosapi.api.auth_url')),
]

