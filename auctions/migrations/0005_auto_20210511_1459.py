# Generated by Django 3.1.4 on 2021-05-11 06:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20210511_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='listing_img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
