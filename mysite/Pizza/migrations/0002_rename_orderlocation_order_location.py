# Generated by Django 4.2.2 on 2023-07-07 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Pizza', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='orderLocation',
            new_name='location',
        ),
    ]