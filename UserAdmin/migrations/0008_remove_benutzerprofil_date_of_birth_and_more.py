# Generated by Django 4.2 on 2025-01-13 19:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("UserAdmin", "0007_benutzerprofil"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="benutzerprofil",
            name="date_of_birth",
        ),
        migrations.RemoveField(
            model_name="benutzerprofil",
            name="profil_image",
        ),
        migrations.RemoveField(
            model_name="benutzerprofil",
            name="some_file",
        ),
    ]
