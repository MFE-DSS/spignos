from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, ChatAPI, ConversationMessagesAPI

router = DefaultRouter()
router.register(r'chats', ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
    path('conversations/', ConversationMessagesAPI.as_view(), name='conversations'),
]
