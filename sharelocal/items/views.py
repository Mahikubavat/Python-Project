from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item
from .forms import ItemForm


def item_list(request):
    """List all available items. Supports ?nearby=1&lat=X&lng=Y&radius=N for GPS filtering."""
    items = Item.objects.filter(status='Available').select_related('owner', 'category')

    nearby = request.GET.get('nearby')
    user_lat = request.GET.get('lat')
    user_lng = request.GET.get('lng')
    radius_km = float(request.GET.get('radius', 20))

    items_with_distance = []

    if nearby and user_lat and user_lng:
        try:
            user_lat = float(user_lat)
            user_lng = float(user_lng)
            for item in items:
                dist = item.distance_to(user_lat, user_lng)
                if dist is not None and dist <= radius_km:
                    items_with_distance.append((item, round(dist, 2)))
            items_with_distance.sort(key=lambda x: x[1])
        except (ValueError, TypeError):
            items_with_distance = [(item, None) for item in items]
    else:
        items_with_distance = [(item, None) for item in items]

    context = {
        'items_with_distance': items_with_distance,
        'nearby_mode': bool(nearby and user_lat and user_lng),
        'radius_km': radius_km,
        'total_items': Item.objects.filter(status='Available').count(),
    }
    return render(request, 'items/item_list.html', context)


@login_required(login_url='login')
def add_item(request):
    """Add a new item. GPS coordinates captured from browser."""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.latitude = form.cleaned_data.get('latitude') or None
            item.longitude = form.cleaned_data.get('longitude') or None
            item.save()
            messages.success(request, f'"{item.title}" listed successfully!')
            return redirect('item_detail', pk=item.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ItemForm()

    return render(request, 'items/add_item.html', {'form': form})


def item_detail(request, pk):
    """Show item detail. Pass whether the current user has already requested it."""
    item = get_object_or_404(Item, pk=pk)
    user_has_requested = False
    if request.user.is_authenticated:
        from request_app.models import ItemRequest
        user_has_requested = ItemRequest.objects.filter(
            item=item, requested_by=request.user
        ).exists()
    return render(request, 'items/item_detail.html', {
        'item': item,
        'user_has_requested': user_has_requested,
    })


@login_required(login_url='login')
def my_items(request):
    """Items listed by the current user."""
    user_items = Item.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'items/my_items.html', {'user_items': user_items})
