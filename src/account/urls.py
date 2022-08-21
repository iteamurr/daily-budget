from django.urls import path

from .views import signin_view
from .views import CreateAccountView
from .views import LoginAccountView
from .views import LogoutAccountView


app_name = "account"
urlpatterns = [
    path("", signin_view, name="signin"),
    path("signup/", CreateAccountView.as_view(), name="create_account"),
    path("login/", LoginAccountView.as_view(), name="login"),
    path("logout/", LogoutAccountView.as_view(), name="logout"),
]
