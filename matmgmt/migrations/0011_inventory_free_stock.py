# Generated by Django 3.2 on 2021-05-11 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matmgmt', '0010_reservation_consumed'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='free_stock',
            field=models.BooleanField(default='False', verbose_name='Free Stock'),
        ),
    ]
