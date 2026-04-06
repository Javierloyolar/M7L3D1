from django.urls import path
from . import views

urlpatterns = [
    path("authors/create/", views.create_author),
    path("books/", views.list_books),
    path("books/create/", views.create_book),
]