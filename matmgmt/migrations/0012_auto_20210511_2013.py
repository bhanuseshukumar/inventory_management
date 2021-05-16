# Generated by Django 3.2 on 2021-05-11 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matmgmt', '0011_inventory_free_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='secondary_loc',
            field=models.CharField(default='default', help_text='Enter slot/pack Number', max_length=30),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='comment',
            field=models.CharField(blank=True, help_text='Add an optional remark for what it is reserved for easy reference', max_length=100),
        ),
        migrations.AlterField(
            model_name='stockissue',
            name='comment',
            field=models.CharField(blank=True, help_text='Add an optional remark for where it is used for easy reference', max_length=100),
        ),
        migrations.AlterField(
            model_name='storelocation',
            name='primary_loc',
            field=models.CharField(help_text='Enter cupboard or drawer number', max_length=30),
        ),
    ]