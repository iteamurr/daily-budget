from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import CreateUserForm
from .forms import UserLoginForm


def signin_view(request):
    if request.user.is_authenticated:
        return redirect("budget/")
    else:
        return redirect("login/")


class CreateAccountView(CreateView):
    form_class = CreateUserForm
    success_url: str = reverse_lazy("login")
    template_name: str = "account/create_account.html"


class LoginAccountView(LoginView):
    form_class = UserLoginForm
    next_page: str = "/budget/"
    redirect_authenticated_user: bool = True
    template_name: str = "account/login.html"


class LogoutAccountView(LogoutView):
    next_page: str = "/login/"
