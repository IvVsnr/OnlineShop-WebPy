# Generated by Django 4.2 on 2024-12-13 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Onlineshop', '0004_rename_bild_produktbild_bilder'),
    ]

    operations = [
        migrations.AddField(
            model_name='produkt',
            name='produkt_bild',
            field=models.ImageField(blank=True, null=True, upload_to='produkt_bilder/'),
        ),
        migrations.DeleteModel(
            name='ProduktBild',
        ),
    ]
