from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from order.models import Order

@staff_member_required
def dashboard_view(request):
    selected_date = request.GET.get('tanggal', None)
    orders = Order.objects.all().order_by('-created_at')
    
    if selected_date:
        orders = orders.filter(created_at__date=selected_date)
    

    context = {
        'orders': orders,
        'selected_date': selected_date,
    }
    return render(request, 'dashboard/dashboard.html', context)

@staff_member_required
def order_detail_view(request, order_id):
    # Ambil pesanan yang spesifik, atau tampilkan 404 jika tidak ada
    order = get_object_or_404(Order, id=order_id)
    
    context = {
        'order': order
    }
    return render(request, 'dashboard/order_detail.html', context)

@staff_member_required
@require_POST # Hanya bisa diakses via metode POST dari form
def approve_payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Ubah status menjadi 'Paid' (Lunas) dan set is_paid menjadi True
    order.status = Order.OrderStatus.PAID
    order.is_paid = True
    order.save()
    
    messages.success(request, f"Pesanan #{order.id} telah ditandai LUNAS.")
    return redirect('dashboard:main') # Kembali ke halaman utama dasbor

@staff_member_required
@require_POST # Hanya bisa diakses via metode POST dari form
def reject_payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Ubah status menjadi 'Canceled' (Dibatalkan)
    order.status = Order.OrderStatus.CANCELED
    order.save()

    messages.warning(request, f"Pesanan #{order.id} telah DIBATALKAN.")
    return redirect('dashboard:main') # Kembali ke halaman utama dasbor

@staff_member_required
@require_POST
def mark_as_paid_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Hanya ubah status jika metodenya Cash dan statusnya Pending
    if order.payment_method == 'Cash' and order.status == Order.OrderStatus.PENDING:
        order.status = Order.OrderStatus.PAID
        order.is_paid = True
        order.save()
        messages.success(request, f"Pesanan #{order.id} telah ditandai LUNAS.")
    else:
        messages.error(request, "Aksi tidak valid untuk pesanan ini.")
        
    return redirect('dashboard:main')

@staff_member_required
@require_POST
def process_order_view(request, order_id):
    """Mengubah status pesanan dari 'Lunas' menjadi 'Sedang Disiapkan'."""
    order = get_object_or_404(Order, id=order_id)
    if order.status == Order.OrderStatus.PAID:
        order.status = Order.OrderStatus.PROCESSING
        order.save()
        messages.info(request, f"Pesanan #{order.id} sekarang sedang diproses.")
    return redirect('dashboard:main')

@staff_member_required
@require_POST
def complete_order_view(request, order_id):
    """Mengubah status pesanan dari 'Sedang Disiapkan' menjadi 'Selesai'."""
    order = get_object_or_404(Order, id=order_id)
    if order.status == Order.OrderStatus.PROCESSING:
        order.status = Order.OrderStatus.COMPLETED
        order.save()
        messages.success(request, f"Pesanan #{order.id} telah diselesaikan.")
    return redirect('dashboard:main')