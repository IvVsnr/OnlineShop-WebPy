#from django.contrib.auth.models import User
from django.db import models

from OnlineShopProject import settings
from UserAdmin.models import MyUser


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
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='produkt_created_by',
        related_query_name='produkt_created_by',
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.name} / {self.beschreibung} / {self.produkt_typ} / {self.preis}'

    def durchschnittsterne(self):
        bewertungen = self.bewertungen.all()
        if bewertungen.exists():
            total_sterne = 0
            for b in bewertungen:
                total_sterne += b.sterne if b.sterne is not None else 0  # Falls sterne None ist, wird 0 verwendet
            return total_sterne / bewertungen.count() if bewertungen.count() > 0 else 0  # Vermeidet Division durch 0
        return 0
    #wieso wird das produkt mit 2 sternen nicht angezeigt?


class Comment(models.Model):    #Kommentar kann man dalassen, jetzt noch Sterne berwertung hinzufügen und hilfreich oder nicht und melde funktion.

    text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE, related_name='bewertungen')
    sterne = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        unique_together = ('produkt', 'user')  # Ein User kann nur einmal ein Produkt bewerten.

    def upvotes(self):
        return self.votes.filter(up_or_down='H').count()

    def downvotes(self):
        return self.votes.filter(up_or_down='N').count()

    def vote(self, user, up_or_down):
        # Prüfen, ob der Benutzer bereits abgestimmt hat
        existing_vote = self.votes.filter(user=user).first()

        if existing_vote:
            # Überprüfen, ob der Benutzer dieselbe Wahl erneut trifft
            if existing_vote.up_or_down == up_or_down:
                return False  # Keine Änderung vorgenommen
            else:
                # Ändere die vorhandene Stimme
                existing_vote.up_or_down = up_or_down
                existing_vote.save()
                return True

        # Abstimmung hinzufügen
        Vote.objects.create(comment=self, user=user, up_or_down=up_or_down)
        return True

    def meldungen(self):
        return self.melden.filter(melden='M').count()

    def meld(self, user, melden):
        # Prüfen, ob der Benutzer bereits abgestimmt hat
        existing_meldung = self.melden.filter(user=user).first()

        if existing_meldung:
            # Überprüfen, ob der Benutzer dieselbe Wahl erneut trifft
            if existing_meldung.melden == melden:
                return False  # Keine Änderung vorgenommen
            else:
                # Ändere die vorhandene Stimme
                existing_meldung.melden = melden
                existing_meldung.save()
                return True

        # Abstimmung hinzufügen
        Melden.objects.create(comment=self, user=user, melden=melden)
        return True

    def get_comment_excerpt(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text

    def __str__(self):
        return f'{self.get_comment_excerpt()} ({self.user.username})'

    def __repr__(self):
        return f'{self.get_comment_excerpt()} ({self.user.username} / {self.sterne} / {str(self.timestamp)})'

#class Bewertung(models.Model):
#    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE, related_name='bewertungen')
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    sterne = models.PositiveIntegerField()
#    erstellt_am = models.DateTimeField(auto_now_add=True)

#    class Meta:
#        unique_together = ('produkt', 'user')  # Ein User kann nur einmal ein Produkt bewerten.

#    def __str__(self):
#        return f'{self.produkt} / {self.user}'

#    def __repr__(self):
#        return f'{self.produkt} / {self.user} / {self.sterne} / {self.erstellt_am}'

class Vote(models.Model):

    VOTE_TYPES = [
        ('H', 'hilfreich'),
        ('N', 'nicht hilfreich'),
    ]

    up_or_down = models.CharField(max_length=1, choices=VOTE_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes')

    class Meta:
        unique_together = ('user', 'comment')  # Verhindert, dass ein Benutzer mehrfach für denselben Kommentar abstimmt

    def __str__(self):
        return f'{self.up_or_down} on {self.comment} by {self.user.username}'

    def __repr__(self):
        return f'{self.up_or_down} on {self.comment} by {self.user.username} ({self.timestamp})'

class Melden(models.Model):

    MELDEN_TYPES = [
        ('M', 'melden')
    ]

    melden = models.CharField(max_length=1, choices=MELDEN_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='melden')

    class Meta:
        unique_together = ('user', 'comment')  # Verhindert, dass ein Benutzer mehrfach für denselben Kommentar abstimmt

    def __str__(self):
        return f'{self.melden} on {self.comment} by {self.user.username}'

    def __repr__(self):
        return f'{self.melden} on {self.comment} by {self.user.username} ({self.timestamp})'