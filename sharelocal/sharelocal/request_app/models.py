from django.db import models
from django.contrib.auth.models import User
from items.models import Item
# Create your models here.

class ItemRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    requested_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requested_by.username} -> {self.item.title}"