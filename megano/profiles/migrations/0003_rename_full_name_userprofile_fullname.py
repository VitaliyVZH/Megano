# Generated by Django 5.0 on 2024-01-05 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_rename_avatar_useravatar_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='full_name',
            new_name='fullName',
        ),
    ]
