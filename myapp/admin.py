from django.contrib import admin
from .models import Order
from .models import Product, Category

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total_price', 'created_at')
    search_fields = ('customer_name', 'customer_email')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

