import datetime

from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre, Author
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.constants import (
    LOAN_STATUS_AVAILABLE,
    LOAN_STATUS_MAINTENANCE,
    LOAN_STATUS_ON_LOAN,
    PAGINATION_BY,
    WEEK_DEFAULT,
)
from catalog.form import RenewBookForm


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


class LoanedBooksByUserListView(generic.ListView):

    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = PAGINATION_BY

    def get_queryset(self):
        """Return the books on loan to the current user."""
        return BookInstance.objects.filter(
            borrower=self.request.user, status__exact=LOAN_STATUS_ON_LOAN
        ).order_by("due_back")


@permission_required("catalog.can_mark_returned")
@permission_required("catalog.can_edit")
def my_view(request):
    pass


@login_required
@permission_required("catalog.can_mark_returned", raise_exception=True)
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian.
    """
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        form = RenewBookForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Process the data in form.cleaned_data
            book_instance.due_back = form.cleaned_data["renewal_date"]
            book_instance.save()

            # Redirect to a new URL
            return HttpResponseRedirect(reverse("all-borrowed"))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(
            weeks=WEEK_DEFAULT
        )
        form = RenewBookForm(initial={"renewal_date": proposed_renewal_date})

    context = {
        "form": form,
        "book_instance": book_instance,
    }

    return render(request, "catalog/book_renew_librarian.html", context)


class AuthorCreate(CreateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]
    initial = {"date_of_death": "11/06/2020"}


class AuthorUpdate(UpdateView):
    model = Author
    # Tránh dùng '__all__' nếu model có trường nhạy cảm hoặc không nên cho sửa
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy("authors")


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = PAGINATION_BY


class AuthorDetailView(generic.DetailView):
    model = Author
