from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path("", views.note, name="index"),
    path("notes/create", views.create_note, name="create_note")
]