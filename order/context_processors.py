def cart_item_count(request):
    """
    Menghitung jumlah total item dalam keranjang belanja dari session.
    """
    cart = request.session.get('cart', {})
    
    # Menjumlahkan semua nilai 'quantity' dari setiap item di keranjang
    count = sum(item['quantity'] for item in cart.values())
    
    # Mengembalikan dictionary yang akan tersedia di semua template
    return {'cart_item_count': count}