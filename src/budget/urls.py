from django.urls import path

from .views import BudgetView
from .views import CategoriesView
from .views import AddCategoryView
from .views import CategoryEditView
from .views import CategoryDeleteView
from .views import ItemsView
from .views import AddItemView
from .views import ItemEditView
from .views import ItemDeleteView


app_name = "budget"
urlpatterns = [
    path("", BudgetView.as_view(), name="index"),
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("categories/add/", AddCategoryView.as_view(), name="add_category"),
    path(
        "categories/edit/<str:slug>",
        CategoryEditView.as_view(),
        name="edit_category",
    ),
    path(
        "categories/delete/<str:slug>",
        CategoryDeleteView.as_view(),
        name="delete_category",
    ),
    path("items/", ItemsView.as_view(), name="items"),
    path("items/add/", AddItemView.as_view(), name="add_item"),
    path(
        "items/edit/<int:pk>",
        ItemEditView.as_view(),
        name="edit_item",
    ),
    path(
        "items/delete/<int:pk>",
        ItemDeleteView.as_view(),
        name="delete_item",
    ),
]
