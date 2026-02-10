from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import UserRegistrationForm, UserProfileForm, UserLoginForm
from .models import UserProfile
from request_app.models import ItemRequest


@require_http_methods(["GET", "POST"])
def register(request):
    """
    Handle user registration with UserProfile creation
    """
    if request.user.is_authenticated:
        return redirect('home')  # Redirect if already logged in
    
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Create user
            user = user_form.save(commit=False)
            user.save()
            
            # Create user profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        else:
            # Pass form errors to template
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/register.html', context)


@require_http_methods(["GET", "POST"])
def user_login(request):
    """
    Handle user login with email or username support
    """
    if request.user.is_authenticated:
        return redirect('home')  # Redirect if already logged in
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Try to authenticate with username first
            user = authenticate(request, username=username_or_email, password=password)
            
            # If not found, try with email
            if user is None:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                
                # Redirect to next page if provided
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username/email or password.')
    else:
        form = UserLoginForm()
    
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def user_logout(request):
    """
    Handle user logout
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    """
    Display user profile with request statistics
    """
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)
    
    # Get request statistics
    pending_received = ItemRequest.objects.filter(
        item__owner=request.user,
        status='Pending'
    ).count()
    
    accepted_received = ItemRequest.objects.filter(
        item__owner=request.user,
        status='Accepted'
    ).count()
    
    pending_sent = ItemRequest.objects.filter(
        requested_by=request.user,
        status='Pending'
    ).count()
    
    accepted_sent = ItemRequest.objects.filter(
        requested_by=request.user,
        status='Accepted'
    ).count()
    
    # Get recent requests
    recent_received = ItemRequest.objects.filter(
        item__owner=request.user
    ).select_related('requested_by', 'item').order_by('-requested_date')[:5]
    
    context = {
        'user_profile': user_profile,
        'pending_received': pending_received,
        'accepted_received': accepted_received,
        'pending_sent': pending_sent,
        'accepted_sent': accepted_sent,
        'recent_received': recent_received,
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def edit_profile(request):
    """
    Edit user profile information
    """
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserProfileForm(instance=user_profile)
    
    context = {'form': form}
    return render(request, 'accounts/edit_profile.html', context)