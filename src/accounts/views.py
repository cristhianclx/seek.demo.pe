# -*- coding: utf-8 -*-

from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response

from base.mixins import SerializerMixin

from .models import User
from .serializers import UserCreateSerializer, UserPasswordChangeSerializer, UserSerializer


class AuthLoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": UserSerializer(user).data,
            }
        )


class AccountsViewSet(
    SerializerMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    permission_classes_by_action = {
        "users_create": [
            permissions.AllowAny,
        ],
    }
    serializer_class = UserSerializer
    serializer_class_by_action = {
        "users_create": UserCreateSerializer,
        "users_update": UserSerializer,
        "user_password_change": UserPasswordChangeSerializer,
    }

    filterset_fields = []
    search_fields = []
    ordering_fields = []

    def get_instance(self) -> User:
        return self.request.user

    @action(
        detail=False,
        methods=["post"],
        url_path="users",
    )
    def users_create(self, request, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        serializer = self.get_serializer(
            data=request.data,
            *args,
            **kwargs,
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        data = serializer.validated_data
        instance.is_active = True
        instance.set_password(data.get("password"))
        instance.save()
        context = self.serializer_class(instance).data
        return Response(context, status=status.HTTP_201_CREATED)

    @users_create.mapping.patch
    def users_update(self, request, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        serializer = self.get_serializer(
            self.get_instance(),
            data=request.data,
            partial=True,
            *args,
            **kwargs,
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        context = self.serializer_class(instance).data
        return Response(context)

    @action(
        detail=False,
        methods=["post"],
        url_path="users/password-change",
        url_name="user_password_change",
        serializer_class=UserPasswordChangeSerializer,
    )
    def user_password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data.get("old_password")
        new_password = serializer.validated_data.get("new_password")
        if not self.get_instance().check_password(old_password):
            return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
        self.get_instance().set_password(new_password)
        self.get_instance().save()
        return Response(status=status.HTTP_204_NO_CONTENT)
