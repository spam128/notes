from django.urls import path

from notes.notebook.views import NoteCreateView, NoteListView, NoteUpdateView

app_name = "users"
urlpatterns = [
    path("create/", view=NoteCreateView.as_view(), name="note-create"),
    path("flowers/", view=NoteListView.as_view(), name="flower-list"),
    path("flowers/<slug:pk>/", view=NoteUpdateView.as_view(), name="note-detail"),
]
