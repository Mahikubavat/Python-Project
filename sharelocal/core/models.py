from django.db import models
from django.utils import timezone


class Category(models.Model):
    """
    Category for items on the platform.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)  # For Bootstrap icons
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Location(models.Model):
    """
    Location/Area model for better location management.
    """
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['city', 'name']
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        if self.state:
            return f"{self.name}, {self.city}, {self.state}"
        return f"{self.name}, {self.city}"
