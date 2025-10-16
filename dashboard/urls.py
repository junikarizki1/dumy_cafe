from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='main'),
    path('order/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('order/mark-as-paid/<int:order_id>/', views.mark_as_paid_view, name='mark_as_paid'),
    path('order/process/<int:order_id>/', views.process_order_view, name='process_order'),
    path('order/complete/<int:order_id>/', views.complete_order_view, name='complete_order'),
    path('order/approve/<int:order_id>/', views.approve_payment_view, name='approve_payment'),
    path('order/reject/<int:order_id>/', views.reject_payment_view, name='reject_payment'),
]