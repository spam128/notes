from django.urls import path

from notes.notebook.views import NoteCreateView, NoteListView, NoteUpdateView, CategoryCreateView, TypeCreateView, NoteByCategoryListView

app_name = "users"
urlpatterns = [
    path("note/add/", view=NoteCreateView.as_view(), name="note-add"),
    path("note/", view=NoteListView.as_view(), name="note-list"),
    path("note/category/<int:pk>", view=NoteByCategoryListView.as_view(), name="note-category-list"),
    path("flowers/<slug:pk>/", view=NoteUpdateView.as_view(), name="note-detail"),
    path("food/", view=NoteListView.as_view(), name="food_recipes-list"),

    path("category/add", view=CategoryCreateView.as_view(), name="category-add"),

    path("type/add", view=TypeCreateView.as_view(), name="type-add"),

]
