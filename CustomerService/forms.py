from django import forms
from Onlineshop.models import Comment, Produkt


class CommentEditForm(forms.ModelForm):

    class Meta:

        model = Comment
        fields = ['text']

        widgets = {
            'comment_id': forms.HiddenInput(),
        }

class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Produkt
        fields = ['name', 'beschreibung', 'preis', 'produkt_bild', 'produkt_pdf', 'produkt_typ']

        widgets = {'produkt_id': forms.HiddenInput(),}