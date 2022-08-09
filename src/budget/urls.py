from django.urls import path

from .views import (
    BudgetView,
    CategoriesView,
    CategoryFormView,
    CategoryEditView,
    CategoryDeleteView,
)


app_name = "budget"
urlpatterns = [
    path("", BudgetView.as_view(), name="index"),
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("categories/add/", CategoryFormView.as_view(), name="add_category"),
    path(
        "categories/edit/<slug:slug>",
        CategoryEditView.as_view(),
        name="edit_category",
    ),
    path(
        "categories/delete/<slug:slug>",
        CategoryDeleteView.as_view(),
        name="delete_category",
    ),
]
