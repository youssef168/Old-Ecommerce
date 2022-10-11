from django.contrib import admin
from .models import Product , Review, Order, OrderProduct, ShippingAddress

# Register your models here.

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)