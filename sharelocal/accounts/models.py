from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def save(self, *args, **kwargs):
        """Update all user's items when location changes."""
        # Check if location has changed
        if self.pk:
            try:
                old_profile = UserProfile.objects.get(pk=self.pk)
                if old_profile.location != self.location:
                    # Update all items owned by this user
                    from items.models import Item
                    Item.objects.filter(owner=self.user).update(location=self.location)
            except UserProfile.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username