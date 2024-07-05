# -*- coding:UTF-8 -*-

from django.http import HttpResponse


def CORSMiddleware(get_response):
    def middleware(request):
        if request.method == "OPTIONS":
            response = HttpResponse()
            response["Content-Length"] = "0"
        else:
            response = get_response(request)
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Headers"] = ", ".join(
            [
                "accept",
                "accept-encoding",
                "authorization",
                "content-type",
                "dnt",
                "origin",
                "user-agent",
                "x-csrftoken",
                "x-requested-with",
            ]
        )
        response["Access-Control-Allow-Methods"] = ", ".join(
            [
                "OPTIONS",
                "HEAD",
                "GET",
                "POST",
                "PUT",
                "PATCH",
                "DELETE",
            ]
        )
        response["Access-Control-Allow-Origin"] = "*"
        return response

    return middleware
