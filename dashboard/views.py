from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from order.models import Order

@staff_member_required
def dashboard_view(request):
    # Ambil pesanan yang perlu perhatian: yang menunggu konfirmasi atau yang sudah lunas tapi belum diproses
    orders = Order.objects.filter(
        status__in=[Order.OrderStatus.WAITING_CONFIRMATION, Order.OrderStatus.PAID]
    ).order_by('created_at') # Tampilkan yang paling lama masuk di urutan pertama

    context = {
        'orders': orders
    }
    return render(request, 'dashboard/dashboard.html', context)