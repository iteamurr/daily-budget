from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UsernameField


class CreateUserForm(UserCreationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"class": "form__elem-input"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form__elem-input", "autocomplete": "new-password"}
        ),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(
            attrs={"class": "form__elem-input", "autocomplete": "new-password"}
        ),
    )


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"class": "form__elem-input", "autofocus": True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form__elem-input", "autocomplete": "current-password"}
        )
    )
