import django_filters


class CategoryFilter(django_filters.FilterSet):
    CHOICES = (
        ("acs", "Items (ascending)"),
        ("desc", "Items (descending)"),
    )
    name = django_filters.CharFilter(label="Category name", lookup_expr="icontains")
    ordering = django_filters.ChoiceFilter(
        label="Order", choices=CHOICES, method="filter_by_order"
    )

    def filter_by_order(self, queryset, name, value):
        expression = "num" if value == "acs" else "-num"
        return queryset.order_by(expression)


class ItemFilter(django_filters.FilterSet):
    CHOICES = (
        ("date_acs", "Date (ascending)"),
        ("date_desc", "Date (descending)"),
        ("cost_acs", "Cost (ascending)"),
        ("cost_desc", "Cost (descending)"),
    )
    title = django_filters.CharFilter(label="Title", lookup_expr="icontains")
    category = django_filters.CharFilter(
        label="Category", field_name="category__name", lookup_expr="icontains"
    )
    ordering = django_filters.ChoiceFilter(
        label="Order", choices=CHOICES, method="filter_by_order"
    )

    def filter_by_order(self, queryset, name, value):
        if "cost" in value:
            expression = "cost" if "acs" in value else "-cost"
        else:
            expression = "date" if "acs" in value else "-date"
        return queryset.order_by(expression)
