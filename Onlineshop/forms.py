from django import forms

from Onlineshop.models import Produkt, Comment


class ProductForm(forms.ModelForm):

    class Meta:
        model = Produkt
        #fields = '__all__'
        exclude = ['user']
        widgets = {
            'produkt_bild': forms.ClearableFileInput(attrs={'multiple': False}),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = ['text', 'sterne']

        widgets = {
            'user': forms.HiddenInput(),
            'sterne': forms.Select(choices=[(i, f"{i} Sterne") for i in range(1, 6)]),
            'produkt': forms.HiddenInput(),
        }

class CommentEditForm(forms.ModelForm):

    class Meta:

        model = Comment
        fields = ['text', 'sterne']

        widgets = {
            'user': forms.HiddenInput(),
            'comment_id': forms.HiddenInput(),
            'sterne': forms.Select(choices=[(i, f"{i} Sterne") for i in range(1, 6)]),
            'produkt': forms.HiddenInput(),
        }



class SearchForm(forms.ModelForm):

    name = forms.CharField(required=False)
    preis = forms.IntegerField(required=False)
    beschreibung = forms.CharField(required=False)
    sterne = forms.IntegerField(required=False)

    class Meta:
        model = Comment
        fields = ['name', 'preis', 'beschreibung', 'sterne']

#class BewertungsForm(forms.ModelForm):
#    class Meta:
#        model = Bewertung
#        fields = ['sterne']
#        widgets = {
#            'sterne': forms.Select(choices=[(i, f"{i} Sterne") for i in range(1, 6)]),
#        }