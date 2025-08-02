# electronics/admin.py
from django.contrib import admin
from .models import Category, Product, Order, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'price', 'stock', 'condition')
    list_filter = ('category', 'condition')
    search_fields = ('name', 'description')
    raw_id_fields = ('seller', 'category')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'product', 'quantity', 'total_price', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('buyer__username', 'product__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('product__name', 'user__username')