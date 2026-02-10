from django import forms
from .models import ItemRequest


class RequestItemForm(forms.ModelForm):
    class Meta:
        model = ItemRequest
        fields = []  # User and Item are set in the view


class RequestStatusForm(forms.ModelForm):
    class Meta:
        model = ItemRequest
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control'
            })
        }
