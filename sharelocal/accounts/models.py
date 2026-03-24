from django.contrib.auth.models import User
from django.db import models
import requests

def geocode_location(location):
    """Geocode a location string to get latitude and longitude."""
    if not location:
        return None, None
    
    try:
        # Using Nominatim API (OpenStreetMap) - free and no API key required
        url = f"https://nominatim.openstreetmap.org/search"
        params = {
            'q': location,
            'format': 'json',
            'limit': 1
        }
        headers = {
            'User-Agent': 'ShareLocal/1.0'
        }
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except (requests.RequestException, ValueError, KeyError, IndexError):
        pass
    
    return None, None

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def save(self, *args, **kwargs):
        """Update all user's items when location changes."""
        location_changed = False
        if self.pk:
            try:
                old_profile = UserProfile.objects.get(pk=self.pk)
                if old_profile.location != self.location:
                    location_changed = True
            except UserProfile.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
        
        # Update all items owned by this user if location changed
        if location_changed:
            from items.models import Item
            lat, lon = geocode_location(self.location)
            Item.objects.filter(owner=self.user).update(
                location=self.location,
                latitude=lat,
                longitude=lon
            )

    def __str__(self):
        return self.user.username