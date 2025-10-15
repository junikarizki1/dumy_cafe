from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Import
from django.conf.urls.static import static # Import


urlpatterns = [
path('admin/', admin.site.urls),
path('', include('core.urls')),
path('menu/', include('menu.urls')),
path('order/', include('order.urls')),
path('users/', include('users.urls')),
path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)