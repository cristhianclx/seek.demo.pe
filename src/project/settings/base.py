# -*- coding: utf-8 -*-

from datetime import timedelta
from os import path as os_path

from rest_framework.settings import api_settings
from unipath import Path as unipath__Path

##
## debug
##

DEBUG = False


##
## security
##

SECRET_KEY = "+z#31^rpf!=)(3mt5o%_dq^5qyk2lgts0m)ue0-xn(4@y)&cr^"


##
## configuration
##

BASE_DIR = unipath__Path(__file__).ancestor(3)

PROJECT_ROOT = BASE_DIR

ALLOWED_HOSTS = []


##
## apps
##

INSTALLED_APPS = [
    # apps
    "accounts",
    "base",
    "main",
    "me",
    # django
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # others
    "django_filters",
    "rest_framework",
    "knox",
    "drf_yasg",  # docs
    # site
    "jazzmin",
    "django.contrib.admin",
]

LOGIN_URL = "/admin/login/"


##
## middleware
##

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "base.middleware.CORSMiddleware",  # CORS
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


##
## URL's
##

ROOT_URLCONF = "project.urls"


##
## templates
##

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os_path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "debug": DEBUG,
        },
    }
]


##
## deploy
##

WSGI_APPLICATION = "project.wsgi.application"


##
## password validators
##

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 6,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


##
## I18N & L18N
##

LANGUAGE_CODE = "en"
TIME_ZONE = "America/Lima"

USE_I18N = True
USE_L10N = False
USE_TZ = True

PHONENUMBER_DB_FORMAT = "E164"

DATE_FORMAT = "d/m/Y"
SHORT_DATE_FORMAT = "d/m/Y"
TIME_FORMAT = "h:i:s A"

LOCALE_PATHS = [
    os_path.join(BASE_DIR, "locale"),
]


##
## static
##

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os_path.join(BASE_DIR, "static"),
]

STATIC_ROOT = os_path.join(BASE_DIR, "static-files")


##
## users
##

AUTH_USER_MODEL = "accounts.User"

SESSION_EXPIRE_AT_BROWSER_CLOSE = True


##
## DRF
##

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "knox.auth.TokenAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "base.utils.Pagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ),
    "COERCE_DECIMAL_TO_STRING": False,
}


##
## knox
##

KNOX_TOKEN_MODEL = "knox.AuthToken"

REST_KNOX = {
    "AUTH_TOKEN_CHARACTER_LENGTH": 64,
    "TOKEN_TTL": timedelta(hours=10),
    "USER_SERIALIZER": "accounts.serializers.UserSerializer",
    "TOKEN_LIMIT_PER_USER": None,
    "AUTO_REFRESH": False,
    "MIN_REFRESH_INTERVAL": 60,
    "AUTH_HEADER_PREFIX": "Token",
    "EXPIRY_DATETIME_FORMAT": api_settings.DATETIME_FORMAT,
    "TOKEN_MODEL": "knox.AuthToken",
}


##
## API
##

API_PREFIX = "api/"


##
## API - docs
##

DOCS_DESCRIPTION = "API - Documentation for SEEK"
DOCS_TITLE = "API"

DOCS_VERSION = "v1"
DOCS_CONTACT = "seek@demo.pe"
DOCS_LICENSE = "Apache-2.0"


##
## website
##

WEBSITE_NAME = "SEEK"


##
## jazzmin
##

JAZZMIN_SETTINGS = {
    "site_logo": "img/logo.png",
    "site_logo_classes": "img-circle",
    "site_icon": "ico/favicon.ico",
    "welcome_sign": WEBSITE_NAME,
    "copyright": " - SEEK ♥",
    "search_model": ["accounts.User", "main.Book"],
    "user_avatar": None,
    "topmenu_links": [],
    "usermenu_links": [],
    "show_sidebar": True,
    "navigation_expanded": False,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "accounts",
        "main",
        "knox",
    ],
    "icons": {
        "accounts": "fas fa-users-cog",
        "accounts.user": "fas fa-user",
        "main": "fas fa-star",
        "main.book": "fas fa-book",
        "knox": "fas fa-sign",
        "knox.token": "fas fa-sign-in-alt",
    },
    "default_icon_parents": "fas fa-book",
    "default_icon_children": "fas fa-book-open",
    "related_modal_active": False,
    "custom_css": "css/admin.min.css",
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {},
    "language_chooser": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "journal",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
    "actions_sticky_top": True,
}


##
## logging
##

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
}
