from django.urls import path

from .views import (
    BudgetView,
    CategoriesView,
    CategoryFormView,
    CategoryEditView,
    CategoryDeleteView,
    ItemsView,
    ItemFormView,
    ItemEditView,
    ItemDeleteView,
)


app_name = "budget"
urlpatterns = [
    path("", BudgetView.as_view(), name="index"),
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("items/", ItemsView.as_view(), name="items"),
    path("categories/add/", CategoryFormView.as_view(), name="add_category"),
    path("items/add/", ItemFormView.as_view(), name="add_item"),
    path(
        "categories/edit/<slug:slug>",
        CategoryEditView.as_view(),
        name="edit_category",
    ),
    path(
        "items/edit/<int:pk>",
        ItemEditView.as_view(),
        name="edit_item",
    ),
    path(
        "categories/delete/<slug:slug>",
        CategoryDeleteView.as_view(),
        name="delete_category",
    ),
    path(
        "items/delete/<int:pk>",
        ItemDeleteView.as_view(),
        name="delete_item",
    ),
]
