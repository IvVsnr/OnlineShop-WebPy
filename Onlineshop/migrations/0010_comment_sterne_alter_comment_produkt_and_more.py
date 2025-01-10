# Generated by Django 4.2 on 2024-12-28 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Onlineshop", "0009_bewertung"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="sterne",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="comment",
            name="produkt",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bewertungen",
                to="Onlineshop.produkt",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="comment",
            unique_together={("produkt", "user")},
        ),
        migrations.DeleteModel(
            name="Bewertung",
        ),
    ]
