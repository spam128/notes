from django.urls import path

from notes.notebook.views import NoteCreateView, NoteListView, NoteUpdateView

app_name = "users"
urlpatterns = [
    path("create/", view=NoteCreateView.as_view(), name="note-create"),
    path("flowers/", view=NoteListView.as_view(), name="flowers-list"),
    path("flowers/<slug:pk>/", view=NoteUpdateView.as_view(), name="note-detail"),
    path("food/", view=NoteListView.as_view(), name="food_recipes-list"),

]
