from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from menu.models import ListMenu
from decimal import Decimal
from django.contrib import messages

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