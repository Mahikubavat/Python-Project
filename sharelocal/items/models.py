from django.db import models
from django.contrib.auth.models import User
from core.models import Category

class Item(models.Model):
    """
    Model for items that users can share on the platform.
    """
    ITEM_TYPE_CHOICES = [
        ('Share', 'Share'),
        ('Sell', 'Sell'),
        ('Rent', 'Rent'),
    ]
    STATUS_CHOICES = [
        ("available", "Available"),
        ("sold", "Sold"),
        ("pending", "Pending"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, default="Share")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="items/", blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    
