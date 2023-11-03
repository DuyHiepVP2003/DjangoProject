from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image_link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Items'
    def __str__(self):
        return self.name