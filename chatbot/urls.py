from django.urls import path
from . import views
from .views import generate_content
from django.shortcuts import render

urlpatterns = [
    path('chat/', views.chat_with_gemini, name='chat'),
    path('check-api-key/', views.example_view, name='check_api_key'),
    path('generate-content/', views.generate_content, name='generate_content'),
    path("chat/", lambda request: render(request, "chat.html"), name="chat"),
]
