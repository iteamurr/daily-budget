from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from .models import Category


class CategoryForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        slug = slugify(cleaned_data.get("name"))
        exists = Category.objects.filter(slug=slug).exists()

        if exists:
            raise ValidationError("A similar name already exists.")

    class Meta:
        model = Category
        fields = ["name"]

        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}
