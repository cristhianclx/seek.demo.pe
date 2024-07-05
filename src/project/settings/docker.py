# -*- coding: utf-8 -*-

from project.settings.base import *

STAGE = "docker"


##
## debug
##

DEBUG = True


##
## configuration
##

ALLOWED_HOSTS = ["*"]


##
## templates
##

TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG


##
## databases
##

DATABASE_HOST = "database"
DATABASE_PORT = 27017
DATABASE_NAME = "bbdd"
DATABASE_USERNAME = "user"
DATABASE_PASSWORD = "password"
DATABASE_AUTHSOURCE = "admin"

DATABASES = {
    "default": {
        "ENGINE": "djongo",
        "NAME": DATABASE_NAME,
        "ENFORCE_SCHEMA": True,
        "CLIENT": {
            "host": DATABASE_HOST,
            "port": DATABASE_PORT,
            "username": DATABASE_USERNAME,
            "password": DATABASE_PASSWORD,
            "authSource": DATABASE_AUTHSOURCE,
        },
    }
}


##
## DRF
##

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += ("rest_framework.renderers.BrowsableAPIRenderer",)
