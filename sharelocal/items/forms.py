from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    """
    Form for creating and editing items.
    """
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'item_type', 'price', 'image']
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
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }
