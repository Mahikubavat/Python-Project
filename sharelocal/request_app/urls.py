from django.urls import path
from . import views

urlpatterns = [
    path('request/<int:item_id>/', views.request_item, name='request_item'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('incoming/', views.incoming_requests, name='incoming_requests'),
    path('accept/<int:req_id>/', views.accept_request, name='accept_request'),
    path('reject/<int:req_id>/', views.reject_request, name='reject_request'),
    path('cancel/<int:req_id>/', views.cancel_request, name='cancel_request'),
]
