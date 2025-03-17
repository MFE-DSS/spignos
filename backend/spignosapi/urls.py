"""
URL configuration for spignosapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import ChatAPI, CreateConversation, ListConversations

urlpatterns = [
    path('conversation/create/', CreateConversation.as_view(), name="create_conversation"),
    path('conversations/<int:user_id>/', ListConversations.as_view(), name="list_conversations"),
    path('chat/', ChatAPI.as_view(), name="chat_api"),  # ✅ Endpoint principal
    path('chat/<int:conversation_id>/', ChatAPI.as_view(), name="chat_conversation"),
]
