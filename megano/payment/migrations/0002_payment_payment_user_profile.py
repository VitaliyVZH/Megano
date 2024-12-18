# Generated by Django 5.0 on 2024-09-27 06:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        ('profiles', '0012_remove_userprofile_avatar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_user_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='profiles.userprofile'),
            preserve_default=False,
        ),
    ]
