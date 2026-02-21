from django.db import models
from django.contrib.auth.models import User
from core.models import Category

class Item(models.Model):
    """
    Model for items that users can share on the platform.
    """
    ITEM_TYPE_CHOICES = [
        # internal value remains 'Share' for backward compatibility, display updated to "Give Away"
        ('Share', 'Give Away'),
        ('Sell', 'Sell'),
        ('Rent', 'Rent'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, default='Share')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default="available")  # ← ADD HERE

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def clean(self):
        """Ensure price rules are followed depending on item type."""
        from django.core.exceptions import ValidationError
        if self.item_type == 'Share' and self.price:
            raise ValidationError('Give away items cannot have a price.')
        if self.item_type in ['Sell', 'Rent'] and not self.price:
            raise ValidationError('Selling or renting items require a price.')

    def __str__(self):
        return self.title

    



