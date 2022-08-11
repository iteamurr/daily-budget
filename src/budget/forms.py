from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import Category
from .models import Item


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(CategoryForm, self).__init__(*args, **kwargs)

        self.fields["name"].queryset = Category.objects.filter(user=self.user)

    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()

        slug = slugify(cleaned_data.get("name"))
        exists = self.fields["name"].queryset.filter(slug=slug).exists()

        if exists:
            raise ValidationError("A similar name already exists.")

    class Meta:
        model = Category
        fields = ["name"]

        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}


class ItemForm(forms.ModelForm):
    time = forms.TimeField(
        widget=forms.TimeInput(
            format="%H:%M", attrs={"class": "form-control", "type": "time"}
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ItemForm, self).__init__(*args, **kwargs)

        self.fields["category"].queryset = Category.objects.filter(user=self.user)
        if "instance" in kwargs and kwargs["instance"]:
            self.fields["time"].initial = kwargs["instance"].date.time()

    def save(self, commit=True):
        item = super(ItemForm, self).save(commit=False)
        item.date = datetime.combine(
            self.cleaned_data["date"], self.cleaned_data["time"]
        )
        if commit:
            item.save()
        return item

    class Meta:
        model = Item
        fields = ["date", "time", "title", "cost", "category"]

        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "cost": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }
