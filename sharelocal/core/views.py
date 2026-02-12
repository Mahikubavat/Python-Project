from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from items.models import Item
from request_app.models import ItemRequest

def home(request):
    """
    Home page view with featured items and request stats
    """
    # Get featured items (latest 6)
    featured_items = Item.objects.filter(status='Available').order_by('-created_at')[:6]
    
    # Get statistics
    total_items = Item.objects.count()
    total_requests = ItemRequest.objects.count()
    total_users = Item.objects.values('owner').distinct().count()
    
    # Get pending count for logged-in users
    pending_count = 0
    if request.user.is_authenticated:
        pending_count = ItemRequest.objects.filter(
            item__owner=request.user,
            status='Pending'
        ).count()
    
    context = {
        'featured_items': featured_items,
        'total_items': total_items,
        'total_requests': total_requests,
        'total_users': total_users,
        'pending_count': pending_count,
    }
    return render(request, 'core/home.html', context)