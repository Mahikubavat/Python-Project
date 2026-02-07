from django.db import models
from django.contrib.auth.models import User
from core.models import Category
# Create your models here.

class Item(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Requested', 'Requested'),
        ('Given', 'Given'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='items/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title