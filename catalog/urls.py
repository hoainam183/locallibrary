from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.BookListView.as_view(), name="books"),
    path("book/<int:pk>", views.book_detail_view, name="book-detail"),
]
