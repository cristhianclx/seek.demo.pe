# -*- coding: utf-8 -*-

from django.utils.translation import gettext_lazy as _

BOOK_GENRE_FICTION = "FICTION"
BOOK_GENRE_NON_FICTION = "NON_FICTION"
BOOK_GENRE_SCIENCE = "SCIENCE"
BOOK_GENRE_HISTORY = "HISTORY"

BOOK_GENRE_CHOICES = [
    (BOOK_GENRE_FICTION, _("Fiction")),
    (BOOK_GENRE_NON_FICTION, _("Non-fiction")),
    (BOOK_GENRE_SCIENCE, _("Science")),
    (BOOK_GENRE_HISTORY, _("History")),
]
