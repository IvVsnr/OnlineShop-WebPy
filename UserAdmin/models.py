from django.contrib.auth.models import AbstractUser
from django.db import models
import random

class MyUser(AbstractUser):

    USER_TYPES = [
        ('SU', 'superuser'),
        ('CS', 'customer support'),
        ('CU', 'customer user'),
        ('QA', 'quality assurance')
    ]

    type = models.CharField(
        max_length=2,
        choices=USER_TYPES,
        default='SU'
    )

    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)

    some_file = models.FileField(upload_to='uploaded_files', blank=True, null=True)

    gets_discount = models.BooleanField(default=False)

    def has_delete_permission(self):
        return self.is_superuser_or_customer_support()
        #return self.is_superuser_or_staff()

    def execute_after_login(self):
        user_gets_randomly_selected_for_discount = random.choice([True, False])

        if user_gets_randomly_selected_for_discount:
            self.gets_discount = True
            self.save()


    def is_superuser_or_customer_support(self):
        return self.type == 'SU' or self.type == 'CS'

    def is_superuser_or_staff(self):
        return self.is_superuser or self.is_staff

    def __str__(self):
        return f'{self.first_name} {self.last_name} )'