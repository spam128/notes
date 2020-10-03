from django.urls import path

from notes.notebook.views import NoteCreateView, NoteListView, NoteUpdateView, CategoryCreateView, TypeCreateView, \
    NoteByCategoryListView, NoteDeleteView

app_name = "users"
urlpatterns = [
    path("add/<int:type>/", view=NoteCreateView.as_view(), name="note-add"),
    path("<int:pk>", view=NoteListView.as_view(), name="note-list"),
    path("category/<int:pk>/", view=NoteByCategoryListView.as_view(), name="note-category-list"),
    path("<int:pk>/", view=NoteUpdateView.as_view(), name="note-detail"),
    path("update/<int:pk>/", view=NoteUpdateView.as_view(), name="note-update"),
    path("delete/<int:pk>/", view=NoteDeleteView.as_view(), name="note-delete"),


    path("category/add", view=CategoryCreateView.as_view(), name="category-add"),

    path("type/add", view=TypeCreateView.as_view(), name="type-add"),

]
