"""config URL Configuration
"""
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("account.urls")),
    path("", include("django.contrib.auth.urls")),
    path("budget/", include("budget.urls")),
]
