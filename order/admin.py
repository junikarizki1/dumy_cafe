from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import format_html

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_type', 'table_number', 'is_paid', 'created_at']
    list_filter = ['is_paid', 'created_at', 'order_type']
    list_editable = ['is_paid'] 
    inlines = [OrderItemInline]
    
    readonly_fields = ('display_payment_proof',)
    def display_payment_proof(self, obj):
        if obj.payment_proof:
            return format_html('<a href="{}"><img src="{}" width="150" /></a>', obj.payment_proof.url, obj.payment_proof.url)
        return "Tidak ada bukti"
    display_payment_proof.short_description = "Bukti Pembayaran"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity',]