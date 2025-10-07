from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from menu.models import ListMenu
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

# Untuk saat ini kita belum membuat model Order, jadi view ini hanya fokus pada logika session

@require_POST # Memastikan view ini hanya bisa diakses dengan metode POST
def add_to_cart(request, product_id):
    # Dapatkan objek produk dari database
    product = get_object_or_404(ListMenu, id=product_id)
    
    # Ambil keranjang dari session, atau buat keranjang kosong jika belum ada
    cart = request.session.get('cart', {})
    
    # Ambil kuantitas dari form (defaultnya 1)
    quantity = int(request.POST.get('quantity', 1))
    
    product_id_str = str(product.id)

    # Jika produk sudah ada di keranjang, tambahkan kuantitasnya
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += quantity
    # Jika belum ada, tambahkan produk baru ke keranjang
    else:
        cart[product_id_str] = {
            'quantity': quantity,
            'price': str(product.price), # Simpan harga sebagai string
            'name': product.name,
        }

    # Simpan kembali keranjang yang sudah diperbarui ke dalam session
    request.session['cart'] = cart
    # Notif produk berhasil ditambahkan ke keranjang
    messages.warning(request, f"'{product.name}' Berhasil ditambahkan ke Pesanan!")
    # Arahkan pengguna kembali ke halaman daftar menu
    return redirect('menu:list_menu')


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = Decimal('0.00')

    # Buat salinan keys untuk iterasi agar kita bisa mengubah cart di dalam loop
    product_ids_in_cart = list(cart.keys()) 

    for product_id in product_ids_in_cart:
        try:
            product = ListMenu.objects.get(id=int(product_id))
            item_data = cart[product_id]
            subtotal = Decimal(item_data['price']) * item_data['quantity']
            
            cart_items.append({
                'product': product,
                'quantity': item_data['quantity'],
                'price': Decimal(item_data['price']),
                'subtotal': subtotal
            })
            total_price += subtotal
        except ListMenu.DoesNotExist:
            # Jika produk tidak ditemukan di database, hapus dari session cart
            del request.session['cart'][product_id]
            request.session.modified = True # Tandai session sebagai termodifikasi

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'order/cart_detail.html', context)

# Fungsi hapus
def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    # Periksa apakah produk ada di keranjang
    if product_id_str in cart:
        product_name = cart[product_id_str]['name'] # Ambil nama untuk notifikasi
        # Hapus produk dari dictionary cart
        del cart[product_id_str]
        # Simpan kembali session yang sudah dimodifikasi
        request.session.modified = True
        # Beri notifikasi sukses
        messages.error(request, f"'{product_name}' Telah Dihapus dari Pesanan.")
    # Arahkan pengguna kembali ke halaman keranjang
    return redirect('order:cart_detail')

@login_required # Memastikan hanya user yang login yang bisa checkout
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        # Jika keranjang kosong, arahkan kembali ke halaman menu
        messages.error(request, "Keranjang Anda kosong.")
        return redirect('menu:list_menu')

    # Logika untuk menangani pengiriman form (POST request)
    if request.method == 'POST':
        order_type = request.POST.get('order_type')
        table_number = request.POST.get('table_number')
        
        if order_type == 'Dine-In':
            table_number = request.POST.get('table_number')
            if not table_number:
                messages.error(request, "Nomor meja wajib diisi untuk pesanan Dine-In.")
                return redirect('order:checkout')
        
        payment_method = request.POST.get('payment_method')
        
        # 1. Buat objek Order baru di database
        order = Order.objects.create(
            user=request.user, 
            table_number=table_number,
            order_type=order_type,
            payment_method=payment_method
        )

        # 2. Loop melalui item di keranjang dan buat OrderItem untuk masing-masing
        for product_id, item_data in cart.items():
            product = get_object_or_404(ListMenu, id=int(product_id))
            OrderItem.objects.create(
                order=order,
                product=product,
                price=Decimal(item_data['price']),
                quantity=item_data['quantity']
            )

        # 3. Hapus keranjang dari session setelah pesanan dibuat
        del request.session['cart']
        request.session.modified = True
        
        # 4. Beri notifikasi sukses dan arahkan ke halaman 'order success'
        messages.success(request, "Terima kasih! Pesanan Anda telah diterima dan sedang kami proses.")
        return redirect('order:order_success',order_id=order.id)

    # Logika untuk menampilkan halaman (GET request)
    # Ini tidak berubah, hanya untuk menampilkan ringkasan
    cart_items = []
    total_price = Decimal('0.00')
    for product_id, item_data in cart.items():
        product = get_object_or_404(ListMenu, id=int(product_id))
        subtotal = Decimal(item_data['price']) * item_data['quantity']
        cart_items.append({
            'product': product,
            'quantity': item_data['quantity'],
            'price': Decimal(item_data['price']),
            'subtotal': subtotal
        })
        total_price += subtotal
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'order/checkout.html', context)


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order
    }
    return render(request, 'order/order_success.html', context)

@login_required
@require_POST
def upload_proof(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Ambil file yang diupload dari form
    payment_proof_file = request.FILES.get('payment_proof')

    if payment_proof_file:
        # Simpan file ke field model Order
        order.payment_proof = payment_proof_file
        # Ubah status pesanan
        order.status = Order.OrderStatus.WAITING_CONFIRMATION
        order.save()
        messages.success(request, "Bukti pembayaran berhasil diupload.")
    else:
        messages.error(request, "Anda harus memilih file untuk diupload.")

    # Arahkan pengguna kembali ke halaman sukses yang sama
    return redirect('order:order_history')

@login_required
def order_history(request):
    # Ambil semua pesanan milik user yang sedang login, urutkan dari yang terbaru
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders
    }
    return render(request, 'order/order_history.html', context)