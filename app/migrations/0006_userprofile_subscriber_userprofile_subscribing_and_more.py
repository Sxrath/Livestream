# Generated by Django 5.0 on 2024-01-08 10:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_userprofile_follower_userprofile_following_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='subscriber',
            field=models.ManyToManyField(related_name='subscriber_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='subscribing',
            field=models.ManyToManyField(related_name='subscribing_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
