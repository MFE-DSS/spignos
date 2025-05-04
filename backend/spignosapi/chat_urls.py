from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import chat_page, home_page

urlpatterns = [
    path("", login_required(chat_page), name="chat"),
    path("home/", home_page, name="home"),
]
