# -*- coding: utf-8 -*-

from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import BOOK_GENRE_CHOICES


class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        verbose_name=_("ID"),
        default=uuid4,
        editable=False,
        unique=True,
    )
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
        blank=False,
    )
    author = models.CharField(
        verbose_name=_("Author"),
        max_length=255,
        blank=False,
    )
    published_date = models.DateField(
        verbose_name=_("Published date"),
        blank=False,
    )
    genre = models.CharField(
        verbose_name=_("Genre"),
        max_length=100,
        blank=False,
        choices=BOOK_GENRE_CHOICES,
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=6,
        decimal_places=2,
        blank=False,
    )
    created = models.DateTimeField(
        verbose_name=_("Created"),
        auto_now_add=True,
        db_index=True,
    )
    updated = models.DateTimeField(
        verbose_name=_("Updated"),
        auto_now=True,
    )

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        indexes = [
            models.Index(fields=["published_date"]),
            models.Index(fields=["price"]),
            models.Index(fields=["published_date", "price"]),
        ]
        ordering = [
            "-created",
        ]
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
