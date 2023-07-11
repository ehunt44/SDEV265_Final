# Generated by Django 4.2.2 on 2023-07-07 19:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Pizza', '0004_order_order_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='Order Date',
        ),
        migrations.AddField(
            model_name='order',
            name='time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]