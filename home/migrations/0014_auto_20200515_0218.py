# Generated by Django 3.0.3 on 2020-05-14 23:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20200513_1902'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calculate',
            old_name='date_buy',
            new_name='date_end',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='date_buy',
            new_name='date_end',
        ),
        migrations.AddField(
            model_name='calculate',
            name='date_start',
            field=models.CharField(default=django.utils.timezone.now, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='date_start',
            field=models.CharField(default=django.utils.timezone.now, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='calculate',
            name='day',
            field=models.IntegerField(),
        ),
    ]