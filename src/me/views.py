# -*- coding: utf-8 -*-

from rest_framework import mixins, permissions, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.serializers import UserSerializer


class MeViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_user(self):
        return self.request.user

    def list(self, request: Request, *args, **kwargs):
        user = self.get_user()
        serializer = self.get_serializer(
            user,
            *args,
            **kwargs,
        )
        return Response(serializer.data)
