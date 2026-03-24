from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    """
    Form for creating and editing items.
    Implements validation rules for price depending on type.
    """
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'item_type', 'price', 'image', 'location', 'latitude', 'longitude']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter item title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your item in detail',
                'rows': 5,
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'item_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price (if selling/renting)',
                'step': '0.01',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Auto-filled from your profile',
                'readonly': 'readonly',
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Latitude (e.g. 37.7749)',
                'step': '0.000001',
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Longitude (e.g. -122.4194)',
                'step': '0.000001',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean(self):
        cleaned = super().clean()
        item_type = cleaned.get('item_type')
        price = cleaned.get('price')
        if item_type == 'Share':
            # treat as give away – no price allowed
            if price:
                self.add_error('price', 'Give away items cannot have a price.')
            cleaned['price'] = None
        else:
            # sell or rent requires a price
            if price in (None, ''):
                self.add_error('price', 'Price is required for selling or renting.')
        return cleaned
