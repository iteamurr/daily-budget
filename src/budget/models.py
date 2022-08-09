from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "Category"
        verbose_name_plural = "Categories"


class Item(models.Model):
    title = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=19, decimal_places=2)
    date = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = "Item"
        verbose_name_plural = "Items"
