from django.shortcuts import render, get_object_or_404
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

def menu_detail_view(request, menu_slug):
    # Cari item menu berdasarkan slug, atau tampilkan error 404 jika tidak ada
    item = get_object_or_404(ListMenu, slug=menu_slug)
    
    recommended_items = ListMenu.objects.exclude(slug=menu_slug).order_by('?')[:4]
    
    context = {
        'item': item,
        'recommended_items': recommended_items,
    }
    return render(request, 'menu/menu_detail.html', context)
