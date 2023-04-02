from django.urls import path
from .views import visual ,upload_csv

urlpatterns = [
    path("v", visual, name="visual"),
    path("", upload_csv, name="uploadcsv"),
]