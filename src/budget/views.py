from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.db.models import Count, Sum

from .models import Category, Item
from .forms import CategoryForm, ItemForm
from .filters import CategoryFilter, ItemFilter


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
        context = super(CategoriesView, self).get_context_data(**kwargs)
        context["filter"] = CategoryFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context

    def get_queryset(self):
        queryset = (
            super(CategoriesView, self).get_queryset().annotate(num=Count("item"))
        )
        return queryset


class CategoryFormView(FormView):
    form_class = CategoryForm
    template_name: str = "budget/category/new_category.html"
    success_url: str = "/budget/categories/"

    def form_valid(self, form):
        form.save()
        return super(CategoryFormView, self).form_valid(form)


class CategoryEditView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name: str = "budget/category/edit_category.html"
    success_url: str = "/budget/categories/"


class CategoryDeleteView(DeleteView):
    model = Category
    template_name: str = "budget/category/delete_category.html"
    success_url: str = "/budget/categories/"

    def get_context_data(self, **kwargs):
        context = super(CategoryDeleteView, self).get_context_data(**kwargs)
        context["items"] = Item.objects.filter(category__slug=self.kwargs.get("slug"))
        return context


class ItemsView(ListView):
    model = Item
    template_name: str = "budget/items.html"

    def get_context_data(self, **kwargs):
        context = super(ItemsView, self).get_context_data(**kwargs)
        context["filter"] = ItemFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ItemFormView(FormView):
    form_class = ItemForm
    template_name: str = "budget/item/new_item.html"
    success_url: str = "/budget/items/"

    def form_valid(self, form):
        form.save()
        return super(ItemFormView, self).form_valid(form)


class ItemEditView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name: str = "budget/item/edit_item.html"
    success_url: str = "/budget/items/"


class ItemDeleteView(DeleteView):
    model = Item
    template_name: str = "budget/item/delete_item.html"
    success_url: str = "/budget/items/"
