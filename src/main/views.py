# -*- coding:UTF-8 -*-

from datetime import datetime

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from pymongo import MongoClient
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from base.mixins import SerializerMixin

from .constants import BOOK_GENRE_CHOICES
from .models import Book
from .serializers import BookSerializer


class BookViewSet(
    SerializerMixin,
    viewsets.ModelViewSet,
):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = BookSerializer

    filterset_fields = {
        "title": ["exact", "icontains"],
        "author": ["exact", "icontains"],
        "genre": ["exact"],
    }

    search_fields = [
        "title",
        "author",
    ]
    ordering_fields = [
        "published_date",
        "genre",
        "price",
    ]

    lookup_field = "id"

    queryset = Book.objects.all()

    @action(detail=False, methods=["GET"])
    def genres(self, request):
        return Response([{"id": genre_choice[0], "name": genre_choice[1]} for genre_choice in BOOK_GENRE_CHOICES])

    @action(detail=False, methods=["GET"], url_path="average-price/(?P<year>[0-9]{4})")
    def average_price(self, request, year=None):
        client = MongoClient(
            host=settings.DATABASE_HOST,
            port=settings.DATABASE_PORT,
            username=settings.DATABASE_USERNAME,
            password=settings.DATABASE_PASSWORD,
            authSource=settings.DATABASE_AUTHSOURCE,
        )
        db = client[settings.DATABASE_NAME]
        collection = db.main_book
        pipeline = [
            {"$match": {"published_date": {"$gte": datetime(int(year), 1, 1), "$lt": datetime(int(year) + 1, 1, 1)}}},
            {"$group": {"_id": None, "price_average": {"$avg": "$price"}}},
        ]
        result = list(collection.aggregate(pipeline))
        if result:
            average_price = round(result[0]["price_average"].to_decimal(), 2)
        else:
            average_price = _("No data available for this year.")
        return Response({"year": year, "price": {"average": average_price}})
