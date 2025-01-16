from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


def add_item_to_shopping_cart(myuser, produkt):
    """
    Creates a shopping cart item and
    assigns it to the shopping cart
    of the current user.
    """

    try:
        shopping_cart = ShoppingCart.objects.get(myuser=myuser)
    except ObjectDoesNotExist:
        shopping_cart = ShoppingCart.objects.create(myuser=myuser)

    product_id = produkt.id
    product_name = produkt.name
    price = produkt.preis

    ShoppingCartItem.objects.create(
        product_id=product_id,
        product_name=product_name,
        price=price,
        quantity=1,  # the quantity is hard coded here, for simplicity reasons
        shopping_cart=shopping_cart
    )


class ShoppingCart(models.Model):

    timestamp = models.DateTimeField(default=timezone.now)

    myuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def get_number_of_items(self):

        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=self)
        num_shopping_cart_items = len(shopping_cart_items)

        return num_shopping_cart_items

    def get_total(self):

        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=self)

        total = sum([
            item.price * item.quantity
            for item
            in shopping_cart_items
        ])

        return total


class ShoppingCartItem(models.Model):

    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    quantity = models.IntegerField(default=1)

    shopping_cart = models.ForeignKey(
        ShoppingCart, on_delete=models.CASCADE
    )

class Payment(models.Model):

    credit_card_number = models.CharField(max_length=19)  # format: 1234 5678 9012 3456
    expiry_date = models.CharField(max_length=7)  # format: 01/2026

    amount = models.DecimalField(decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(default=timezone.now)

    myuser = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )