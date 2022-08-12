from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "Category"
        verbose_name_plural = "Categories"
        unique_together = "slug", "user"


class Item(models.Model):
    title = models.CharField(max_length=72)
    cost = models.DecimalField(max_digits=19, decimal_places=2)
    date = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = "Item"
        verbose_name_plural = "Items"
