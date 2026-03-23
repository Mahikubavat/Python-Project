# Generated migration file

from django.db import migrations

def backfill_locations(apps, schema_editor):
    """Backfill item locations from owner profiles"""
    Item = apps.get_model('items', 'Item')
    UserProfile = apps.get_model('accounts', 'UserProfile')
    
    for item in Item.objects.filter(location__isnull=True):
        try:
            profile = UserProfile.objects.get(user=item.owner)
            if profile.location:
                item.location = profile.location
                item.save(update_fields=['location'])
        except UserProfile.DoesNotExist:
            pass

def reverse_backfill(apps, schema_editor):
    """Reverse backfill - clear locations"""
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_item_location'),
    ]

    operations = [
        migrations.RunPython(backfill_locations, reverse_backfill),
    ]
