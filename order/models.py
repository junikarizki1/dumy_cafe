from django.db import models
from django.contrib.auth.models import User
from menu.models import ListMenu

class Order(models.Model):
    # Opsi untuk tipe pesanan
    class OrderType(models.TextChoices):
        DINE_IN = 'Dine-In', 'Dine-In'
        TAKEAWAY = 'Takeaway', 'Takeaway'
    
    class PaymentMethod(models.TextChoices):
        CASH = 'Cash', 'Bayar di Kasir'
        QRIS = 'QRIS', 'QRIS'
    
    class OrderStatus(models.TextChoices):
        PENDING = 'Pending', 'Menunggu Pembayaran'
        WAITING_CONFIRMATION = 'Waiting Confirmation', 'Menunggu Konfirmasi'
        PAID = 'Paid', 'Lunas'
        PROCESSING = 'Processing', 'Sedang Disiapkan'
        COMPLETED = 'Completed', 'Selesai'
        CANCELED = 'Canceled', 'Dibatalkan'

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # Siapa yang memesan
    order_type = models.CharField(max_length=10, choices=OrderType.choices, default=OrderType.DINE_IN)
    table_number = models.CharField(max_length=5, null=True, blank=True) # Nomor meja jika dine-in
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    status = models.CharField(max_length=25, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    payment_proof = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) # Kapan pesanan dibuat
    is_paid = models.BooleanField(default=False) # Status pembayaran
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.id} by {self.user.username if self.user else "Guest"}'

    def get_total_price(self):
        # Menghitung total harga dari semua item di pesanan ini
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ListMenu, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Harga produk saat dibeli
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity