# -*- coding:utf-8 -*-

from collections import OrderedDict
from decimal import Decimal
from uuid import UUID

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.utils.encoding import force_str
from django.utils.functional import Promise

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class LazyEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, Decimal):
            if o % 1 != 0:
                return float(o)
            else:
                return int(o)
        if isinstance(o, Promise):
            return force_str(o)
        return super(LazyEncoder, self).default(o)


def render_to_json(context, status=200):
    response = JsonResponse(
        context,
        encoder=LazyEncoder,
        status=status,
    )
    return response


class Pagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        response = OrderedDict(
            [
                ("count", self.page.paginator.count),
                ("num_pages", self.page.paginator.num_pages),
                ("page", self.page.number),
                ("next", self.get_next_link()),
                ("previous", self.get_previous_link()),
                ("results", data),
            ]
        )
        return Response(response)
