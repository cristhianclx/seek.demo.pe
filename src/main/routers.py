# -*- coding: utf-8 -*-

from rest_framework import routers

from .views import BookViewSet

router = routers.DefaultRouter()
router.register(
    "books",
    BookViewSet,
    basename="books",
)
