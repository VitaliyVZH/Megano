# Generated by Django 5.0 on 2024-08-22 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsale',
            name='c',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
    ]
