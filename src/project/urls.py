# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import handler400, handler403, handler404, handler500, include
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from knox import views as knox_views
from rest_framework import permissions

from accounts.routers import router as router__accounts
from accounts.views import AuthLoginView
from base.views import PINGViewClass
from main.routers import router as router__main
from me.routers import router as router__me

admin.site.site_header = "{} - {}".format(settings.WEBSITE_NAME, settings.STAGE)
admin.site.site_title = "{}".format(settings.WEBSITE_NAME)
admin.site.site_url = reverse_lazy("admin:index")
admin.site.index_title = _("Administration")
admin.site.enable_nav_sidebar = False


schema_view = get_schema_view(
    openapi.Info(
        title=settings.DOCS_TITLE,
        default_version=settings.DOCS_VERSION,
        description=settings.DOCS_DESCRIPTION,
        contact=openapi.Contact(email=settings.DOCS_CONTACT),
        license=openapi.License(name=settings.DOCS_LICENSE),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # index
    path(
        r"",
        TemplateView.as_view(
            template_name="index.txt",
            content_type="text/plain; charset=utf-8",
        ),
    ),
    # SEO
    path(
        r"robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain; charset=utf-8",
        ),
    ),
    # PING
    path(r"ping/", PINGViewClass.as_view(), name="ping"),
    # site
    path(r"admin/", admin.site.urls),
    path(r"i18n/", include("django.conf.urls.i18n")),
    # auth
    path(r"{}auth/login/".format(settings.API_PREFIX), AuthLoginView.as_view(), name="knox_login"),
    path(r"{}auth/logout/".format(settings.API_PREFIX), knox_views.LogoutView.as_view(), name="knox_logout"),
    path(r"{}auth/logout-all/".format(settings.API_PREFIX), knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
    # API
    path(
        r"{}me/".format(settings.API_PREFIX),
        include(router__me.urls),
    ),
    path(
        r"{}accounts/".format(settings.API_PREFIX),
        include(router__accounts.urls),
    ),
    path(
        r"{}main/".format(settings.API_PREFIX),
        include(router__main.urls),
    ),
    # API - auth
    path(
        r"api-auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
    # docs
    path(
        r"docs<str:format>",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        r"docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-docs",
    ),
]

if settings.DEBUG:
    import sys

    if sys.argv[0].endswith("gunicorn"):
        from django.contrib.staticfiles.urls import staticfiles_urlpatterns

        urlpatterns = urlpatterns + staticfiles_urlpatterns()


handler400 = "base.views.handler400"
handler403 = "base.views.handler403"
handler404 = "base.views.handler404"
handler500 = "base.views.handler500"
