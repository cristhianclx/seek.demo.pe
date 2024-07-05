# -*- coding: utf-8 -*-

from os import environ as os__environ

from django.core.asgi import get_asgi_application

os__environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
application = get_asgi_application()
