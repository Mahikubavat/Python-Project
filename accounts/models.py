from django.contrib.auth.models import User
from django.db import models

def geocode_location(location):
    """Geocode a location string to get latitude and longitude."""
    if not location:
        return None, None
    
    try:
        import requests
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
    except Exception:
        # Gracefully handle any errors (including missing requests library)
        pass
    
    return None, None

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True, help_text='User latitude for location services')
    longitude = models.FloatField(null=True, blank=True, help_text='User longitude for location services')
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
        
        # Geocode location if it changed or coordinates are missing
        if location_changed or (self.location and (not self.latitude or not self.longitude)):
            lat, lon = geocode_location(self.location)
            if lat is not None and lon is not None:
                self.latitude = lat
                self.longitude = lon
        
        super().save(*args, **kwargs)
        
        # Update all items owned by this user if location changed
        if location_changed:
            from items.models import Item
            Item.objects.filter(owner=self.user).update(
                location=self.location,
                latitude=self.latitude,
                longitude=self.longitude
            )

    def __str__(self):
        return self.user.username