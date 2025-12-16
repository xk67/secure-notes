from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = "notes"

urlpatterns = [
    path("", views.note, name="index"),
    path("notes/create", views.create_note, name="create_note"),
    path("notes", views.list_notes, name="list_notes"),
    path("notes/<uuid>", views.show_note, name="show_note"),
    path("api/notes", views.api_list_notes),
    path("api/note/<uuid>", views.api_get_note),
    path('api/token', obtain_auth_token)
]