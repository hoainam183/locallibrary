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

# --------------------
# UUID default function
# --------------------
UUID_DEFAULT = uuid.uuid4
