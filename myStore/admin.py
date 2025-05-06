
# Register your models here.
from django.contrib import admin
from .models import (
    Category,
    Brand,
    Product,
    ProductVariant,
    Cart,
    CartItem,
    Order,
    OrderItem
)

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
