# -*- coding: utf-8 -*-

from rest_framework import routers

from .views import AccountsViewSet

router = routers.DefaultRouter()
router.register(
    "",
    AccountsViewSet,
    basename="accounts",
)
