# Generated by Django 5.0 on 2024-01-06 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_remove_useravatar_user_useravatar_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useravatar',
            old_name='avatar',
            new_name='profile',
        ),
    ]
