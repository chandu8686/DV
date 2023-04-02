from django.urls import path
from .views import visual

urlpatterns = [
    path("", visual, name="visual"),
]