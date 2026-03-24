from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('add/', views.add_item, name='add_item'),
    path('my-items/', views.my_items, name='my_items'),
    path('<int:pk>/', views.item_detail, name='item_detail'),
]
