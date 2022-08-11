from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models import Sum

from .models import Category
from .models import Item
from .forms import CategoryForm
from .forms import ItemForm
from .filters import CategoryFilter
from .filters import ItemFilter


class BudgetView(LoginRequiredMixin, ListView):
    template_name: str = "budget/index.html"
    context_object_name: str = "lists"
    login_url: str = "/login/"

    def get_queryset(self):
        categories = (
            Category.objects.filter(user=self.request.user)
            .annotate(num=Count("item"))
            .only("name")
            .order_by("-num")[:5]
        )
        items = (
            Item.objects.filter(user=self.request.user)
            .only("title", "cost")
            .order_by("-date")[:5]
        )
        chart = (
            Category.objects.filter(user=self.request.user)
            .annotate(sum=Sum("item__cost"))
            .only("name")
            .order_by("-item__cost")[:10]
        )
        return dict(categories=categories, items=items, chart=chart)


class CategoriesView(LoginRequiredMixin, ListView):
    model = Category
    template_name: str = "budget/categories.html"
    login_url: str = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = CategoryFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(user=self.request.user)
            .annotate(num=Count("item"))
        )
        return queryset


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name: str = "budget/category/new_category.html"
    success_url: str = "/budget/categories/"
    login_url: str = "/login/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class CategoryEditView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name: str = "budget/category/edit_category.html"
    success_url: str = "/budget/categories/"
    login_url: str = "/login/"

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name: str = "budget/category/delete_category.html"
    success_url: str = "/budget/categories/"
    login_url: str = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = Item.objects.filter(user=self.request.user).filter(
            category__slug=self.kwargs.get("slug")
        )
        return context


class ItemsView(LoginRequiredMixin, ListView):
    model = Item
    template_name: str = "budget/items.html"
    login_url: str = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = ItemFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


class AddItemView(LoginRequiredMixin, CreateView):
    form_class = ItemForm
    template_name: str = "budget/item/new_item.html"
    success_url: str = "/budget/items/"
    login_url: str = "/login/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ItemEditView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name: str = "budget/item/edit_item.html"
    success_url: str = "/budget/items/"
    login_url: str = "/login/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name: str = "budget/item/delete_item.html"
    success_url: str = "/budget/items/"
    login_url: str = "/login/"

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset
