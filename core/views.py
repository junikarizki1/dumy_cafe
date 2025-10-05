from django.shortcuts import render
from menu.models import Category, ListMenu 


def home(request):
    categories = Category.objects.all()
    list_menus = ListMenu.objects.all()
    context = {
        'categories': categories,
        'list_menus': list_menus,}
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def book(request):
    return render(request, 'core/book.html')