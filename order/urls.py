# File: orders/urls.py

from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.order_success, name='order_success'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('upload-proof/<int:order_id>/', views.upload_proof, name='upload_proof'),
    path('history/', views.order_history, name='order_history'),
]