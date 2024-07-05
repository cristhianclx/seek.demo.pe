# -*- coding: utf-8 -*-

from uuid import uuid4

from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        max_length=255,
        default=uuid4,
        unique=False,
        editable=False,
    )
    email = models.EmailField(
        verbose_name=_("email address"),
        max_length=255,
        blank=False,
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "name"]
    EMAIL_FIELD = "email"

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        blank=False,
    )

    def __str__(self):
        return str(self.email)

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __init__(self, *args, **kwargs):
        self._meta.get_field("username").max_length = 255
        self._meta.get_field("username").blank = True
        self._meta.get_field("username").null = True
        self._meta.get_field("password").blank = False
        self._meta.get_field("first_name").blank = True
        self._meta.get_field("last_name").blank = True
        super(User, self).__init__(*args, **kwargs)
