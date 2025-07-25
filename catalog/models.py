from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .constants import MAX_LENGTH, LOAN_STATUS, UUID_DEFAULT
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    """Model representing a book genre."""

    name = models.CharField(
        max_length=MAX_LENGTH["GENRE_NAME"],
        help_text=_("Enter a book genre (e.g. Science Fiction)"),
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""

    title = models.CharField(max_length=MAX_LENGTH["BOOK_TITLE"])
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=MAX_LENGTH["BOOK_SUMMARY"],
        help_text=_("Enter a brief description of the book"),
    )
    isbn = models.CharField(
        "ISBN",
        max_length=MAX_LENGTH["BOOK_ISBN"],
        unique=True,
        help_text=_(
            '13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
        ),
    )
    genre = models.ManyToManyField(
        "Genre",
        help_text=_("Select a genre for this book"),
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "Genre"


class BookInstance(models.Model):
    """Model representing a specific copy of a book."""

    id = models.UUIDField(
        primary_key=True,
        default=UUID_DEFAULT,
        help_text=_("Unique ID for this particular book across whole library"),
    )
    book = models.ForeignKey("Book", on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=MAX_LENGTH["BOOK_INSTANCE_IMPRINT"])
    due_back = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS["CHOICES"],
        blank=True,
        default=LOAN_STATUS["DEFAULT"],
        help_text=_("Book availability"),
    )
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f"{self.id} ({self.book.title})"

    @property
    def is_overdue(self):
        return self.due_back and date.today() > self.due_back


class Author(models.Model):
    """Model representing an author."""

    first_name = models.CharField(max_length=MAX_LENGTH["AUTHOR_NAME"])
    last_name = models.CharField(max_length=MAX_LENGTH["AUTHOR_NAME"])
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
