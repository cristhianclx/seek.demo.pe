# -*- coding: utf-8 -*-

from datetime import date

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .constants import BOOK_GENRE_CHOICES
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    genre = serializers.ChoiceField(choices=BOOK_GENRE_CHOICES)

    def validate_published_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("The publication date cannot be in the future.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(_("The price must be a positive number."))
        return value

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "published_date",
            "genre",
            "price",
            "created",
            "updated",
        )
        read_only_fields = (
            "id",
            "created",
            "updated",
        )
