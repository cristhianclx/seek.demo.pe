# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db.models import Max, Min
from django.utils.translation import gettext_lazy as _

from .models import Book


class YearFilter(admin.SimpleListFilter):
    title = _("Year of publication")
    parameter_name = "published_date__year"

    def lookups(self, request, model_admin):
        year_aggregate = model_admin.model.objects.aggregate(
            min_year=Min("published_date"), max_year=Max("published_date")
        )
        min_year = year_aggregate["min_year"].year if year_aggregate["min_year"] else None
        max_year = year_aggregate["max_year"].year if year_aggregate["max_year"] else None
        if min_year and max_year:
            years = [(str(year), str(year)) for year in range(min_year, max_year + 1)]
            years.reverse()
            return years
        return []

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(published_date__year=self.value())
        return queryset


@admin.register(Book)
class BookAdmin(
    admin.ModelAdmin,
):
    list_display = (
        "id",
        "title",
        "author",
        "published_date",
        "genre",
        "price",
        "created",
        "updated",
    )
    search_fields = (
        "id",
        "title",
        "author",
    )
    list_filter = (
        "genre",
        YearFilter,
    )
