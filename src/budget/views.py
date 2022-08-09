from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.db.models import Count, Sum

from .models import Category, Item
from .forms import CategoryForm
from .filters import CategoryFilter


class BudgetView(ListView):
    template_name: str = "budget/index.html"
    context_object_name: str = "lists"

    def get_queryset(self):
        categories = (
            Category.objects.annotate(num=Count("item"))
            .order_by("-num")
            .only("name")[:5]
        )
        items = Item.objects.order_by("-date")[:5]
        chart = Category.objects.annotate(sum=Sum("item__cost")).only("name")
        return dict(categories=categories, items=items, chart=chart)


class CategoriesView(ListView):
    model = Category
    template_name: str = "budget/categories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = CategoryFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(num=Count("item"))


class CategoryFormView(FormView):
    form_class = CategoryForm
    template_name: str = "budget/category/new_category.html"
    success_url: str = "/budget/categories/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CategoryEditView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name: str = "budget/category/edit_category.html"
    success_url: str = "/budget/categories/"


class CategoryDeleteView(DeleteView):
    model = Category
    template_name: str = "budget/category/delete_category.html"
    success_url: str = "/budget/categories/"
