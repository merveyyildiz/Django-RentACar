# Generated by Django 3.0.3 on 2020-05-15 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_auto_20200515_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quatity',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.CharField(max_length=30),
        ),
    ]
