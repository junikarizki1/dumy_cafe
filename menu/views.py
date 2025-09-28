from django.shortcuts import render

def list_menu(request):
    return render(request, 'menu/menu.html',)
