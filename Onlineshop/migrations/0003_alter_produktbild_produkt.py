# Generated by Django 4.2 on 2024-12-13 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Onlineshop', '0002_remove_produkt_bilder_produktbild'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produktbild',
            name='produkt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bilder', to='Onlineshop.produkt'),
        ),
    ]
