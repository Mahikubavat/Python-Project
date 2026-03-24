from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Item
from .forms import ItemForm
from core.models import Category
import math


def haversine(lat1, lon1, lat2, lon2):
    """Return distance in kilometers between two lat/lon points."""
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def item_list(request):
    """
    Display list of all available items with search and filter functionality.
    """
    items = Item.objects.filter(is_available=True)
    categories = Category.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        items = items.filter(category__id=category_filter)
    
    # Filter by item type
    item_type_filter = request.GET.get('item_type')
    if item_type_filter:
        items = items.filter(item_type=item_type_filter)

    # Location-based nearest search
    user_lat = request.GET.get('lat')
    user_lon = request.GET.get('lon')
    radius_km = request.GET.get('radius')
    nearest_search = False
    if user_lat and user_lon:
        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
            nearest_search = True
            # Default radius to 50km if not specified
            if not radius_km:
                radius_km = 50.0
        except ValueError:
            user_lat = user_lon = None

    if nearest_search:
        items = items.filter(latitude__isnull=False, longitude__isnull=False)
        item_list = []
        for item in items:
            item.distance_km = haversine(user_lat, user_lon, item.latitude, item.longitude)
            item_list.append(item)

        if radius_km:
            try:
                radius_km = float(radius_km)
                item_list = [item for item in item_list if item.distance_km <= radius_km]
            except ValueError:
                pass

        item_list.sort(key=lambda i: i.distance_km)
        items = item_list
    
    # Pagination
    paginator = Paginator(items, 12)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    
    context = {
        'items': items,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'item_type_filter': item_type_filter,
        'user_lat': user_lat,
        'user_lon': user_lon,
        'radius_km': radius_km,
        'nearest_search': nearest_search,
    }
    return render(request, 'items/item_list.html', context)



@login_required
def add_item(request):
    """
    Add a new item to the platform.
    """
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            # Auto-populate location from owner's profile if not already set
            if not item.location:
                try:
                    user_profile = request.user.userprofile
                    item.location = user_profile.location
                except:
                    pass
            item.save()
            messages.success(request, f'Item "{item.title}" has been added successfully!')
            return redirect('item_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ItemForm()
        # Pre-fill location field with owner's profile location
        try:
            user_profile = request.user.userprofile
            form.initial['location'] = user_profile.location
        except:
            pass

    context = {'form': form}
    return render(request, 'items/add_item.html', context)


@login_required
def my_items(request):
    """
    Display items owned by the current user.
    """
    items = Item.objects.filter(owner=request.user).order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter == 'available':
        items = items.filter(is_available=True)
    elif status_filter == 'unavailable':
        items = items.filter(is_available=False)
    
    # Pagination
    paginator = Paginator(items, 10)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    
    context = {
        'items': items,
        'status_filter': status_filter,
    }
    return render(request, 'items/my_items.html', context)


def item_detail(request, item_id):
    """
    Display detailed view of a specific item.
    """
    item = get_object_or_404(Item, id=item_id)
    
    # Get related items from same category
    related_items = Item.objects.filter(
        category=item.category,
        is_available=True
    ).exclude(id=item.id)[:4]
    
    # Check if current user owns this item
    is_owner = request.user == item.owner if request.user.is_authenticated else False

    # fetch owner's profile for contact info
    owner_profile = getattr(item.owner, 'userprofile', None)
    
    context = {
        'item': item,
        'related_items': related_items,
        'is_owner': is_owner,
        'owner_profile': owner_profile,
    }
    return render(request, 'items/item_detail.html', context)


@login_required
def edit_item(request, item_id):
    """
    Edit an existing item (owner only).
    """
    item = get_object_or_404(Item, id=item_id)
    
    # Check ownership
    if item.owner != request.user:
        messages.error(request, 'You do not have permission to edit this item.')
        return redirect('item_list')
    
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            edited_item = form.save(commit=False)
            # Ensure location stays in sync with owner's profile
            try:
                user_profile = request.user.userprofile
                edited_item.location = user_profile.location
            except:
                pass
            edited_item.save()
            messages.success(request, f'Item "{item.title}" has been updated successfully!')
            return redirect('item_detail', item_id=item.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ItemForm(instance=item)
    
    context = {'form': form, 'item': item}
    return render(request, 'items/add_item.html', context)


@login_required
def delete_item(request, item_id):
    """
    Delete an item (owner only).
    """
    item = get_object_or_404(Item, id=item_id)
    
    # Check ownership
    if item.owner != request.user:
        messages.error(request, 'You do not have permission to delete this item.')
        return redirect('item_list')
    
    if request.method == "POST":
        title = item.title
        item.delete()
        messages.success(request, f'Item "{title}" has been deleted successfully!')
        return redirect('my_items')
    
    context = {'item': item}
    return render(request, 'items/delete_item.html', context)


@login_required
def toggle_item_availability(request, item_id):
    """
    Toggle item availability status (owner only).
    """
    item = get_object_or_404(Item, id=item_id)
    
    # Check ownership
    if item.owner != request.user:
        messages.error(request, 'You do not have permission to modify this item.')
        return redirect('item_list')
    
    item.is_available = not item.is_available
    item.save()
    
    status = "available" if item.is_available else "unavailable"
    messages.success(request, f'Item is now marked as {status}.')
    return redirect('my_items')

