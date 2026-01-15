from django.urls import path
from .views import api, web
from .views.api import APILoginView

app_name = "notes"

urlpatterns = [
    path("notes/create", web.create_note, name="create_note"),
    path("notes", web.list_notes, name="list_notes"),
    path("notes/<uuid>", web.view_note, name="view_note"),
    path("api/notes", api.list_notes),
    path('api/note/create', api.create_note),
    path("api/note/<uuid>", api.get_note),
    path('api/token', APILoginView.as_view(), name="api_get_token"),
    path('note/search', web.search_note, name="search_note"),
    path('note/preview', web.preview_note, name="preview_note")
]
