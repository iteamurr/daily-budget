from datetime import datetime
from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from .models import Category, Item


class CategoryForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()

        slug = slugify(cleaned_data.get("name"))
        exists = Category.objects.filter(slug=slug).exists()

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
        super(ItemForm, self).__init__(*args, **kwargs)

        if "instance" in kwargs:
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
