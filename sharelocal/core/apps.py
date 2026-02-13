from django.apps import AppConfig
from django.db.models.signals import post_migrate

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .models import Category

        def create_default_categories(sender, **kwargs):
            # List all default categories you want
            default_categories = ["Electronics", "Clothing", "Books", "Home", "Other"]

            for cat_name in default_categories:
                Category.objects.get_or_create(name=cat_name)

        # Connect the function to run after migrations
        post_migrate.connect(create_default_categories, sender=self)
