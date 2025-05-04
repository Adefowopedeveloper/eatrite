from django.contrib import admin
from .models import Order, OrderItem, Product, Category

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_email', 'phone', 'total_price', 'created_at')
    search_fields = ('customer_name', 'customer_email', 'phone')
    list_filter = ('created_at', 'payment_method')
    readonly_fields = ('created_at', 'total_price')

    fieldsets = (
        ('Customer Info', {
            'fields': ('customer_name', 'customer_email', 'phone')
        }),
        ('Delivery Info', {
            'fields': ('address', 'note')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'total_price')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

    inlines = [OrderItemInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
