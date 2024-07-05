# -*- coding: utf-8 -*-

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "name",
        )
        read_only_fields = ("email",)


class UserCreateSerializer(UserSerializer):
    password = serializers.CharField(
        label=_("Password"),
        required=True,
        style={
            "input_type": "password",
        },
        min_length=4,
        max_length=128,
        write_only=True,
    )
    password_confirm = serializers.CharField(
        label=_("Confirm password"),
        required=True,
        style={
            "input_type": "password",
        },
        min_length=4,
        max_length=128,
        write_only=True,
    )

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + (
            "password",
            "password_confirm",
        )

    def validate(self, data):
        if "email" in data:
            data["email"] = data["email"].lower()
        data = super().validate(data)
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError(
                {
                    "password_confirm": [
                        _("Password's doesn't match."),
                    ],
                }
            )
        data.pop("password_confirm")
        return data


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        label=_("Old Password"),
        required=True,
        style={
            "input_type": "password",
        },
        min_length=4,
        max_length=128,
        write_only=True,
    )
    new_password = serializers.CharField(
        label=_("New Password"),
        required=True,
        style={
            "input_type": "password",
        },
        min_length=4,
        max_length=128,
        write_only=True,
    )
    confirm_password = serializers.CharField(
        label=_("Confirm New Password"),
        required=True,
        style={
            "input_type": "password",
        },
        min_length=4,
        max_length=128,
        write_only=True,
    )

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")
        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "New passwords must match each other."})
        return super().validate(attrs)
