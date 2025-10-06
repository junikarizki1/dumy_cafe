from django.shortcuts import render, get_object_or_404
from .models import Category, ListMenu # Import model
from django.db.models import Q 
from django.shortcuts import render, get_object_or_404

def list_menu(request):
        # Ambil semua objek kategori dan item menu dari database
    categories = Category.objects.all()
    
    query = request.GET.get('q')
    list_menus = ListMenu.objects.all()
    if query:
        list_menus = list_menus.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ). order_by('name')
    else:
        list_menus = ListMenu.objects.all().order_by('name')
    
        # Kirim data tersebut ke template melalui dictionary 'context'
    context = {
        'categories': categories,
        'list_menus': list_menus,
        'query':query,
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
