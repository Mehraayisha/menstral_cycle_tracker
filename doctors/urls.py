# urls.py
from django.urls import path
from . import views
from django.shortcuts import render


urlpatterns = [
    # Add this URL pattern for fetching nearby doctors
    path("get_nearby_doctors/", views.get_nearby_doctors, name='get_nearby_doctors'),
    path("doct/", lambda request: render(request, "doctors.html"), name="doct"),
]
