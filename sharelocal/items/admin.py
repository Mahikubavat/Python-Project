from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for Item model.
    """
    list_display = ('title', 'owner', 'category', 'item_type', 'price', 'is_available', 'created_at')
    list_filter = ('category', 'item_type', 'is_available', 'created_at')
    search_fields = ('title', 'description', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Item Information', {
            'fields': ('title', 'description', 'category', 'image'),
        }),
        ('Item Details', {
            'fields': ('item_type', 'price'),
        }),
        ('Ownership & Status', {
            'fields': ('owner', 'is_available'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return self.readonly_fields + ('owner',)
        return self.readonly_fields
