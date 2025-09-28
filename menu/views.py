from django.shortcuts import render
from .models import Category, ListMenu # Import model

def list_menu(request):
        # Ambil semua objek kategori dan item menu dari database
    categories = Category.objects.all()
    list_menus = ListMenu.objects.all()
    
        # Kirim data tersebut ke template melalui dictionary 'context'
    context = {
        'categories': categories,
        'list_menus': list_menus,
    }
    return render(request, 'menu/menu.html', context)
