# Generated by Django 3.0.3 on 2020-04-17 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='comment',
            name='subject',
            field=models.CharField(max_length=50),
        ),
    ]
