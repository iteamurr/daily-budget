from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .forms import CreateUserForm, UserLoginForm


class CreateAccountView(CreateView):
    form_class = CreateUserForm
    success_url: str = reverse_lazy("login")
    template_name: str = "account/create_account.html"


class LoginAccountView(LoginView):
    form_class = UserLoginForm
    next_page: str = "/budget/"
    template_name: str = "account/login.html"


class LogoutAccountView(LogoutView):
    next_page: str = "/login/"
