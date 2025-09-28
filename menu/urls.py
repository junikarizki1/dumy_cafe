from django.urls import path
from . import views


urlpatterns = [
path('menu/', views.list_menu, name='list_menu'),
]