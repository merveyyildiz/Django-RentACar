# Generated by Django 3.0.3 on 2020-05-15 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_auto_20200515_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculate',
            name='date_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='calculate',
            name='date_start',
            field=models.DateTimeField(),
        ),
    ]