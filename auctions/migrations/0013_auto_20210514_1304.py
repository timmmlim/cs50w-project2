# Generated by Django 3.1.4 on 2021-05-14 05:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20210513_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='listing_comments', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.CharField(default=None, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
