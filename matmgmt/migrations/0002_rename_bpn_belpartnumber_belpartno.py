# Generated by Django 3.2 on 2021-04-25 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matmgmt', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='belpartnumber',
            old_name='bpn',
            new_name='belPartNo',
        ),
    ]
