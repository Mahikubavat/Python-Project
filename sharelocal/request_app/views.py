from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ItemRequest
from items.models import Item


@login_required(login_url='login')
def request_item(request, item_id):
    """Buyer requests to buy an item."""
    item = get_object_or_404(Item, pk=item_id, status='Available')

    if item.owner == request.user:
        messages.error(request, "You cannot request your own item.")
        return redirect('item_detail', pk=item_id)

    existing = ItemRequest.objects.filter(item=item, requested_by=request.user).first()
    if existing:
        messages.warning(request, "You have already requested this item.")
        return redirect('item_detail', pk=item_id)

    ItemRequest.objects.create(item=item, requested_by=request.user)
    # Mark item as Requested
    item.status = 'Requested'
    item.save()
    messages.success(request, f'Request sent for "{item.title}"! The owner will be in touch.')
    return redirect('item_detail', pk=item_id)


@login_required(login_url='login')
def my_requests(request):
    """Requests made BY the logged-in user (buyer view)."""
    requests_made = ItemRequest.objects.filter(
        requested_by=request.user
    ).select_related('item', 'item__owner').order_by('-requested_date')
    return render(request, 'request_app/my_requests.html', {'requests_made': requests_made})


@login_required(login_url='login')
def incoming_requests(request):
    """Requests received ON items owned by the logged-in user (owner view)."""
    reqs = ItemRequest.objects.filter(
        item__owner=request.user
    ).select_related('item', 'requested_by').order_by('-requested_date')
    return render(request, 'request_app/incoming_requests.html', {'incoming': reqs})


@login_required(login_url='login')
def accept_request(request, req_id):
    req = get_object_or_404(ItemRequest, pk=req_id, item__owner=request.user)
    req.status = 'Accepted'
    req.save()
    req.item.status = 'Given'
    req.item.save()
    # Reject all other pending requests for this item
    ItemRequest.objects.filter(item=req.item).exclude(pk=req_id).update(status='Rejected')
    messages.success(request, f'Request accepted! "{req.item.title}" marked as Given.')
    return redirect('incoming_requests')


@login_required(login_url='login')
def reject_request(request, req_id):
    req = get_object_or_404(ItemRequest, pk=req_id, item__owner=request.user)
    req.status = 'Rejected'
    req.save()
    # If no more pending requests, set item back to Available
    if not ItemRequest.objects.filter(item=req.item, status='Pending').exists():
        req.item.status = 'Available'
        req.item.save()
    messages.info(request, 'Request rejected.')
    return redirect('incoming_requests')


@login_required(login_url='login')
def cancel_request(request, req_id):
    req = get_object_or_404(ItemRequest, pk=req_id, requested_by=request.user)
    item = req.item
    req.delete()
    if not ItemRequest.objects.filter(item=item, status='Pending').exists():
        item.status = 'Available'
        item.save()
    messages.info(request, 'Your request has been cancelled.')
    return redirect('my_requests')
