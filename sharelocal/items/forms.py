from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    latitude = forms.FloatField(
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'item_latitude'})
    )
    longitude = forms.FloatField(
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'item_longitude'})
    )

    class Meta:
        model = Item
        fields = ('title', 'description', 'category', 'price', 'location',
                  'latitude', 'longitude', 'image', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Item location / address',
                'id': 'item_location',
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
