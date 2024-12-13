from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Produkt(models.Model):

    class Meta:
        ordering = ['name']
        verbose_name = 'Produkt'
        verbose_name_plural = 'Produkts'

    PRODUKT_TYPES = [
        ('elektronik', 'Elektronik'),
        ('bekleidung', 'Bekleidung'),
        ('moebel', 'Möbel'),
        ('buecher', 'Bücher'),
        ('schmuck', 'Schmuck'),
        ('kosmetik', 'Kosmetik'),
        ('sport', 'Sportartikel'),
        ('lebensmittel', 'Lebensmittel'),
        ('spielzeug', 'Spielzeug'),
        ('haushalt', 'Haushaltswaren'),
        ('geschenke', 'Geschenke'),
        ('gesundheit', 'Gesundheitsprodukte'),
        ('musik', 'Musikinstrumente'),
        ('kunst', 'Kunst und Dekoration'),
        ('software', 'Computersoftware'),
        ('werkzeuge', 'Werkzeuge'),
    ]

    name = models.CharField(max_length=200)
    beschreibung = models.TextField(max_length=1000)
    preis = models.DecimalField(max_digits=10, decimal_places=2)
    produkt_bild = models.ImageField(upload_to='produkt_bilder/', null=True, blank=True)
    produkt_pdf = models.FileField(upload_to='produkt_pdfs/', null=True, blank=True)
    produkt_typ = models.CharField(max_length=100, choices=PRODUKT_TYPES)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='produkts',
        related_query_name='produkt',
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.name} / {self.beschreibung} / {self.produkt_typ} / {self.preis}'


