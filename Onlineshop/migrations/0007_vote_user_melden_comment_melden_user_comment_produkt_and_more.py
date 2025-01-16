# Generated by Django 4.2 on 2025-01-13 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Onlineshop', '0006_comment_melden_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='melden',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='melden', to='Onlineshop.comment'),
        ),
        migrations.AddField(
            model_name='melden',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='produkt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bewertungen', to='Onlineshop.produkt'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('user', 'comment')},
        ),
        migrations.AlterUniqueTogether(
            name='melden',
            unique_together={('user', 'comment')},
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('produkt', 'user')},
        ),
    ]
