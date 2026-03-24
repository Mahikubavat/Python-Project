from django.urls import path
from . import views

urlpatterns = [
    path('requests/', views.request_list, name='request-list'),
    path('my-requests/', views.my_requests, name='my-requests'),
    path('request/<int:request_id>/', views.request_detail, name='request-detail'),
    path('request/create/<int:item_id>/', views.create_request, name='create-request'),
    path('request/<int:request_id>/accept/', views.accept_request, name='accept-request'),
    path('request/<int:request_id>/reject/', views.reject_request, name='reject-request'),
    path('request-history/', views.request_history, name='request-history'),
]
