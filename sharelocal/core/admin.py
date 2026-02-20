from django.contrib import admin
from .models import Category, Location


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.
    """
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'icon'),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Location model.
    """
    list_display = ('name', 'city', 'state', 'zip_code', 'created_at')
    list_filter = ('city', 'state')
    search_fields = ('name', 'city', 'state')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Location Details', {
            'fields': ('name', 'city', 'state', 'zip_code'),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
