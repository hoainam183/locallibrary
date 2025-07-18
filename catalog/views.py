from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.shortcuts import get_object_or_404
from catalog.constants import (
    LOAN_STATUS_AVAILABLE,
    LOAN_STATUS_MAINTENANCE,
    PAGINATION_BY,
)


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact=LOAN_STATUS_AVAILABLE
    ).count()

    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_visits": num_visits,
    }

    # Render the HTML template index.html with the data in the context variable.
    return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = PAGINATION_BY


def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(
        request,
        "catalog/book_detail.html",
        context={
            "book": book,
            "genre_display": book.genre.all,
            "all_bookInstance": book.bookinstance_set.all,
            "STATUS_AVAILABLE": LOAN_STATUS_AVAILABLE,
            "STATUS_MAINTENANCE": LOAN_STATUS_MAINTENANCE,
        },
    )
