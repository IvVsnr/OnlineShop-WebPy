# Generated by Django 4.2 on 2024-12-13 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Onlineshop', '0003_alter_produktbild_produkt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produktbild',
            old_name='bild',
            new_name='bilder',
        ),
    ]
