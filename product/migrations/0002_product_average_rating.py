# Generated by Django 3.2 on 2021-05-17 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='average_rating',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
