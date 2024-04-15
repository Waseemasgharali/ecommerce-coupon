# cart/admin.py

from django.contrib import admin
from .models import Cart, PlaceOrder, Coupon

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product','quantity']

@admin.register(PlaceOrder)
class PlaceOrderModelAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'product','quantity','order_date','status']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percentage', 'valid_from', 'valid_to', 'active']
