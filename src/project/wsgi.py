# -*- coding: utf-8 -*-

from os import environ as os__environ

from django.core.wsgi import get_wsgi_application

os__environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
application = get_wsgi_application()
