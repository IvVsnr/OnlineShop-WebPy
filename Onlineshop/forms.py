from django import forms

from Onlineshop.models import Produkt


class ProductForm(forms.ModelForm):

    class Meta:
        model = Produkt
        #fields = '__all__'
        exclude = ['user']
        widgets = {
            'bilder': forms.ClearableFileInput(attrs={'multiple': True}),
        }