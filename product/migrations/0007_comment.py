# Generated by Django 3.0.3 on 2020-04-16 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0006_auto_20200410_2222'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=50)),
                ('comment', models.TextField(blank=True, max_length=200)),
                ('rate', models.IntegerField(blank=True)),
                ('status', models.CharField(blank=True, choices=[('New', 'Yeni'), ('True', 'Evet'), ('False', 'Hayır')], default='new', max_length=10)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_At', models.DateTimeField(auto_now=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]