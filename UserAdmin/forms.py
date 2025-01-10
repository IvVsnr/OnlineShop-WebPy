from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import BenutzerProfil

# Formular für die Benutzerregestrierung
ROLE_CHOICES = [
    ('customer', 'Kunde'),
    ('customer_service', 'Kunden Service'),
    ('superuser', 'Superuser'),
]

class CustomerUserForm(UserCreationForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label='Benutzerrolle')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data['role']

        if role == 'superuser':
            user.is_superuser = True
            user.is_staff = True
        elif role == 'customer_service':
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff  = False

        if commit:
            user.save()
        return user



class BenutzerProfilForm(forms.ModelForm):
    class Meta:
        model = BenutzerProfil
        fields = ['date_of_birth', 'profil_image', 'some_file']
