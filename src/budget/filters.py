import django_filters

from .models import Category


class CategoryFilter(django_filters.FilterSet):
    CHOICES = (
        ("acs", "Items (ascending)"),
        ("desc", "Items (descending)"),
    )
    name = django_filters.CharFilter(label="Name", lookup_expr="icontains")
    ordering = django_filters.ChoiceFilter(
        label="Order", choices=CHOICES, method="filter_by_order"
    )

    def filter_by_order(self, queryset, name, value):
        expression = "num" if value == "acs" else "-num"
        return queryset.order_by(expression)

    class Meta:
        model = Category
        fields = ["name"]
