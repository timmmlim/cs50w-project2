# Generated by Django 3.1.4 on 2021-05-13 03:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210511_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='curr_bid',
        ),
        migrations.AddField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bid',
            name='is_highest',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
