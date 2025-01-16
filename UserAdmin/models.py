from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
import random

from OnlineShopProject import settings
from ShoppingCart.models import ShoppingCart


class MyUser(AbstractUser):

    USER_TYPES = [
        ('SU', 'superuser'), #admin
        ('CS', 'customer support'), #
        ('CU', 'customer user') #normaler user
    ]

    type = models.CharField(
        max_length=2,
        choices=USER_TYPES,
        default='CU',
    )
    date_of_birth = models.DateField(blank=True, null=True)

    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    some_file = models.FileField(upload_to='uploaded_files', blank=True, null=True)

    def has_delete_permission(self):
        return self.is_superuser_or_customer_support()
        #return self.is_superuser_or_staff()

    def is_superuser_or_customer_support(self):
        return self.type == 'SU' or self.type == 'CS'

    def is_superuser_or_staff(self):
        return self.is_superuser or self.is_staff

    def __str__(self):
        return f'{self.first_name} {self.last_name} )'


    def count_shopping_cart_items(self):

        if not self.is_authenticated:
            return 0

        try:
            shopping_cart = ShoppingCart.objects.get(myuser=self)
            count = shopping_cart.get_number_of_items()

            return count

        except ObjectDoesNotExist:
            print(f'WARNING: User with id {self.id} does not have a shopping cart.')

            return 0

#class BenutzerProfil(models.Model):
#    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profil')
#
#    def __str__(self):
#        return f"{self.user.username} Profil"

