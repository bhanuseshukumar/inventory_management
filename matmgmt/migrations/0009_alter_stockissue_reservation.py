# Generated by Django 3.2 on 2021-04-30 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matmgmt', '0008_auto_20210430_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockissue',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='matmgmt.reservation'),
        ),
    ]
