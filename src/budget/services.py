from django.views.generic import ListView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.db.models import Count
from django.db.models import Sum

from .models import Category
from .models import Item


def get_index_page_lists(
    user, max_categories_list_len: int = 5, max_items_list_len: int = 5
):
    categories = (
        Category.objects.filter(user=user)
        .annotate(num=Count("item"))
        .order_by("-num")[:max_categories_list_len]
    )
    items = Item.objects.filter(user=user).order_by("-date")[:max_items_list_len]
    chart, total = beautify_chart_data(
        Category.objects.filter(user=user)
        .annotate(sum=Sum("item__cost"))
        .order_by("-item__cost")
    )
    return dict(categories=categories, items=items, chart=chart, sum=total)


def beautify_chart_data(data):
    chart, other = {}, 0

    for category in data:
        if category.sum is None:
            continue
        elif category.name in chart:
            chart[category.name] += float(category.sum)
        elif len(chart) > 8:
            other += float(category.sum)
        else:
            chart[category.name] = float(category.sum)

    chart = dict(sorted(chart.items(), key=lambda x: x[1], reverse=True))

    if other:
        chart["Other"] = other

    return chart, sum(chart.values())


class CustomListView(ListView):
    filter_for_pagination = None
    context_object_name = ""

    def get_filtered_and_paginated_data(self, context):
        data = self.request.GET
        queryset = self.filter_for_pagination(data, queryset=self.get_queryset())
        paginator = Paginator(queryset.qs, self.paginate_by)

        try:
            objects = paginator.page(data.get("page"))
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        context["form"] = queryset.form
        context["num_pages"] = paginator.num_pages
        context["page_obj"] = context[self.context_object_name] = objects
        return context
