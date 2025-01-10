from django.contrib import admin
from ShoppingCart.models import ShoppingCart, ShoppingCartItem, Payment

admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(Payment)