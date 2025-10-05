from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
path('menu/', views.list_menu, name='list_menu'),
path('<slug:menu_slug>/', views.menu_detail_view, name='menu_detail'),
]