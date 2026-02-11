from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('add/', views.add_item, name='add_item'),
    path('my/', views.my_items, name='my_items'),
    path('<int:item_id>/', views.item_detail, name='item_detail'),
    path('<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('<int:item_id>/toggle-availability/', views.toggle_item_availability, name='toggle_availability'),
]
