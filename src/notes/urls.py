from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import api, web

app_name = "notes"

urlpatterns = [
    path("notes/create", web.create_note, name="create_note"),
    path("notes", web.list_notes, name="list_notes"),
    path("notes/<uuid>", web.view_note, name="view_note"),
    path("api/notes", api.list_notes),
    path('api/note/create', api.create_note),
    path("api/note/<uuid>", api.get_note),
    path('api/token', obtain_auth_token, name="api_get_token"),
    path('note/search', web.search_note, name="search_note"),
    path('note/preview', web.preview_note, name="preview_note")
]
