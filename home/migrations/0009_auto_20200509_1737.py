# Generated by Django 3.0.3 on 2020-05-09 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20200509_1633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='date_give',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='date_give',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Preaparing', 'Preparing'), ('OnShipping', 'OnShipping'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='New', max_length=10),
        ),
    ]
