"""URL Configuration
"""
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("account.urls")),
    path("", include("django.contrib.auth.urls")),
    path("budget/", include("budget.urls")),
]

handler404 = "config.views.page_not_found_view"
handler500 = "config.views.server_error_view"
