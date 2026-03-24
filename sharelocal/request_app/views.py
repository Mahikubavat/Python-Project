from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from items.models import Item
from .models import ItemRequest
from .forms import RequestItemForm, RequestStatusForm


@login_required
def request_list(request):
    """List all requests for the current user's items"""
    requests = ItemRequest.objects.filter(item__owner=request.user).order_by('-requested_date')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        requests = requests.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(requests, 10)
    page = request.GET.get('page')
    requests = paginator.get_page(page)
    
    context = {
        'requests': requests,
        'status_filter': status_filter,
        'statuses': ItemRequest.STATUS_CHOICES,
    }
    return render(request, 'request_app/request_list.html', context)


@login_required
def my_requests(request):
    """List all requests made by the current user"""
    requests = ItemRequest.objects.filter(requested_by=request.user).order_by('-requested_date')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        requests = requests.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(requests, 10)
    page = request.GET.get('page')
    requests = paginator.get_page(page)
    
    context = {
        'requests': requests,
        'status_filter': status_filter,
        'statuses': ItemRequest.STATUS_CHOICES,
    }
    return render(request, 'request_app/my_requests.html', context)


@login_required
def create_request(request, item_id):
    """Create a new request for an item"""
    item = get_object_or_404(Item, id=item_id)
    
    # Check if user is the owner
    if item.owner == request.user:
        messages.error(request, 'You cannot request your own item.')
        return redirect('item-detail', pk=item_id)

    # Check if user already requested this item and the request is not accepted
    existing_request = ItemRequest.objects.filter(
        item=item,
        requested_by=request.user
    ).exclude(status='Accepted').first()

    if existing_request:
        # simply show the existing request details on the page
        if request.method == 'POST':
            # ignore form submission when a pending/rejected request exists
            messages.warning(request, 'You have already requested this item. See details below.')
        context = {
            'item': item,
            'existing_request': existing_request,
        }
        return render(request, 'request_app/create_request.html', context)

    # create a new request normally
    if request.method == 'POST':
        # Create the request
        item_request = ItemRequest.objects.create(
            item=item,
            requested_by=request.user,
            status='Pending'
        )
        messages.success(request, f'Request for {item.title} has been sent!')
        return redirect('my-requests')

    context = {'item': item}
    return render(request, 'request_app/create_request.html', context)


@login_required
def accept_request(request, request_id):
    """Accept a request for an item"""
    item_request = get_object_or_404(ItemRequest, id=request_id)
    
    # Check if user is the owner of the item
    if item_request.item.owner != request.user:
        messages.error(request, 'You do not have permission to accept this request.')
        return redirect('request-list')
    
    if request.method == 'POST':
        item_request.status = 'Accepted'
        item_request.save()
        
        # Update item status
        item_request.item.status = 'Requested'
        item_request.item.save()
        
        # Reject all other pending requests for this item
        ItemRequest.objects.filter(
            item=item_request.item,
            status='Pending'
        ).exclude(id=item_request.id).update(status='Rejected')
        
        messages.success(request, f'Request from {item_request.requested_by.username} has been accepted!')
        return redirect('request-list')
    
    context = {'request_obj': item_request}
    return render(request, 'request_app/accept_request.html', context)


@login_required
def reject_request(request, request_id):
    """Reject a request for an item"""
    item_request = get_object_or_404(ItemRequest, id=request_id)
    
    # Check if user is the owner of the item
    if item_request.item.owner != request.user:
        messages.error(request, 'You do not have permission to reject this request.')
        return redirect('request-list')
    
    if request.method == 'POST':
        item_request.status = 'Rejected'
        item_request.save()
        messages.success(request, f'Request from {item_request.requested_by.username} has been rejected!')
        return redirect('request-list')
    
    context = {'request_obj': item_request}
    return render(request, 'request_app/reject_request.html', context)


@login_required
def request_detail(request, request_id):
    """View details of a specific request"""
    item_request = get_object_or_404(ItemRequest, id=request_id)
    
    # Check if user is involved in the request
    if item_request.requested_by != request.user and item_request.item.owner != request.user:
        messages.error(request, 'You do not have permission to view this request.')
        return redirect('home')
    
    context = {'request_obj': item_request}
    return render(request, 'request_app/request_detail.html', context)


@login_required
def request_history(request):
    """View request history (both sent and received)"""
    # Get all requests related to the user
    sent_requests = ItemRequest.objects.filter(requested_by=request.user).order_by('-requested_date')
    received_requests = ItemRequest.objects.filter(item__owner=request.user).order_by('-requested_date')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        sent_requests = sent_requests.filter(status=status_filter)
        received_requests = received_requests.filter(status=status_filter)
    
    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
        'status_filter': status_filter,
        'statuses': ItemRequest.STATUS_CHOICES,
    }
    return render(request, 'request_app/request_history.html', context)


@login_required
def pending_requests_count(request):
    """Get count of pending requests for the user's items"""
    if request.user.is_authenticated:
        count = ItemRequest.objects.filter(
            item__owner=request.user,
            status='Pending'
        ).count()
        return {'pending_count': count}
    return {'pending_count': 0}
