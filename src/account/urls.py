from django.urls import path

from .views import CreateAccountView, LoginAccountView, LogoutAccountView


app_name = "account"
urlpatterns = [
    path("", CreateAccountView.as_view(), name="create_account"),
    path("login/", LoginAccountView.as_view(), name="login"),
    path("logout/", LogoutAccountView.as_view(), name="logout"),
]
