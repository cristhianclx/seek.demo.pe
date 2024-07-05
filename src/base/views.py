# -*- coding:UTF-8 -*-

from django.conf import settings
from django.views.defaults import bad_request, page_not_found, permission_denied, server_error
from django.views.generic import View

from .utils import render_to_json


def handler400(request, exception):
    if not request.path.startswith("/{}".format(settings.API_PREFIX)):
        return bad_request(request, exception, template_name="errors/400.html")
    return render_to_json({}, 400)


def handler403(request, exception):
    if not request.path.startswith("/{}".format(settings.API_PREFIX)):
        return permission_denied(
            request,
            template_name="errors/403.html",
            exception=Exception("Permission Denied"),
        )
    return render_to_json({}, 403)


def handler404(request, exception):
    if not request.path.startswith("/{}".format(settings.API_PREFIX)):
        return page_not_found(
            request,
            template_name="errors/404.html",
            exception=Exception("Page not Found"),
        )
    return render_to_json({}, 404)


def handler500(request):
    if not request.path.startswith("/{}".format(settings.API_PREFIX)):
        return server_error(request, template_name="errors/500.html")
    return render_to_json({}, 500)


class PINGViewClass(View):
    def get(self, request):
        context = {
            "stage": settings.STAGE,
            "response": "pong",
        }
        return render_to_json(context)
