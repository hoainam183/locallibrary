from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from constants import LOAN_STATUS_AVAILABLE


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

    # Prepare context for template rendering
    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)
