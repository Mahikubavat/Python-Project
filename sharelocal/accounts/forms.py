from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
import re

class UserRegistrationForm(UserCreationForm):
    """
    Extended registration form with additional fields and validation
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name',
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name',
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username',
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        """Validate that email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_username(self):
        """Validate username format and uniqueness"""
        username = self.cleaned_data.get('username')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        
        # Check username length
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long.')
        
        # Check for valid characters
        if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
            raise forms.ValidationError('Username can only contain letters, numbers, dots, hyphens, and underscores.')
        
        return username

    def clean_password1(self):
        """Validate password strength"""
        password1 = self.cleaned_data.get('password1')
        
        if len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        
        if not re.search(r'[A-Z]', password1):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')
        
        if not re.search(r'[a-z]', password1):
            raise forms.ValidationError('Password must contain at least one lowercase letter.')
        
        if not re.search(r'[0-9]', password1):
            raise forms.ValidationError('Password must contain at least one digit.')
        
        return password1

    def clean(self):
        """Validate that passwords match"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """
    Form for user profile information
    """
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number',
        })
    )
    location = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your location/city',
        })
    )
    profile_photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
        })
    )

    class Meta:
        model = UserProfile
        fields = ('phone', 'location', 'profile_photo')

    def clean_phone(self):
        """Validate phone number"""
        phone = self.cleaned_data.get('phone')
        
        # Remove common separators
        phone_digits = re.sub(r'[\s\-\+\(\)]', '', phone)
        
        # Check if it's all digits
        if not phone_digits.isdigit():
            raise forms.ValidationError('Phone number should contain only digits and common separators.')
        
        # Check length (typically 10-15 digits)
        if len(phone_digits) < 10 or len(phone_digits) > 15:
            raise forms.ValidationError('Phone number should be between 10 to 15 digits.')
        
        return phone


class UserLoginForm(forms.Form):
    """
    Custom login form with validation
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username or email',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
        })
    )

    def clean_username(self):
        """Validate that username exists"""
        username = self.cleaned_data.get('username')
        
        if not User.objects.filter(username=username).exists() and not User.objects.filter(email=username).exists():
            raise forms.ValidationError('Username or email does not exist.')
        
        return username