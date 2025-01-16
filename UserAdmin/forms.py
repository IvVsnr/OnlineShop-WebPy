from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import MyUser

class MySignUpForm(UserCreationForm):

    class Meta:

        model = MyUser

        fields = (
            'username',
            'first_name',
            'last_name',
            'date_of_birth',
            'email',
            'profile_image',
            'some_file'
            # password field is required to be specified explicitly as it is provided by UserCreationForm
        )

class BenutzerProfilForm(forms.ModelForm): #sinnlos
    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'email', 'profile_image', 'some_file']

class UserRechte(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['type']
        #exclude = ['username', 'date_of_birth', ...] #kann vllt weg
        widgets = {'type': forms.Select(attrs={'class': 'form-control'})}
        #Noch html usw anpassen aber die zuweisung funktioniert!!!