# -*- coding: utf-8 -*-

from rest_framework import routers

from .views import MeViewSet

router = routers.DefaultRouter()
router.register("", MeViewSet, basename="me")
