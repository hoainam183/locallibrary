# catalog/constants.py
import uuid

# --------------------
# Max length values
# --------------------
MAX_LENGTH = {
    "GENRE_NAME": 200,
    "AUTHOR_NAME": 100,
    "BOOK_TITLE": 200,
    "BOOK_SUMMARY": 1000,
    "BOOK_ISBN": 13,
    "BOOK_INSTANCE_IMPRINT": 200,
}

# --------------------
# Choices & Defaults
# --------------------
LOAN_STATUS = {
    "CHOICES": [
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    ],
    "DEFAULT": "m",
}

LOAN_STATUS_MAINTENANCE = "m"
LOAN_STATUS_ON_LOAN = "o"
LOAN_STATUS_AVAILABLE = "a"
LOAN_STATUS_RESERVED = "r"

# --------------------
# UUID default function
# --------------------
UUID_DEFAULT = uuid.uuid4

PAGINATION_BY = 2

WEEK_DEFAULT = 3
