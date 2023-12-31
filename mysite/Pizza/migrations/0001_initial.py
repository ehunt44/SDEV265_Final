# Generated by Django 4.2.2 on 2023-07-07 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default Item', max_length=128)),
                ('description', models.CharField(default='Default Description', max_length=256)),
                ('image', models.FilePathField(default='default.png', path='static/Pizza/', recursive=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('calories', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ItemOrderJoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemQuantity', models.IntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Pizza.item')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default Location', max_length=128)),
                ('address', models.CharField(default='Default Address', max_length=128)),
                ('city', models.CharField(default='Default City', max_length=64)),
                ('stateAbriv', models.CharField(default='AA', max_length=2)),
                ('zip', models.CharField(default='12345', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default Topping', max_length=64)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('calories', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalCost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('customerName', models.CharField(default='Default Customer Name', max_length=128)),
                ('customerAddress', models.CharField(default='Default Customer Address', max_length=128)),
                ('items', models.ManyToManyField(through='Pizza.ItemOrderJoin', to='Pizza.item')),
                ('orderLocation', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Pizza.location')),
            ],
        ),
        migrations.AddField(
            model_name='itemorderjoin',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pizza.order'),
        ),
        migrations.AddField(
            model_name='itemorderjoin',
            name='toppings',
            field=models.ManyToManyField(db_table='ItemToppingOrderJoin', to='Pizza.topping'),
        ),
        migrations.AddField(
            model_name='item',
            name='toppings',
            field=models.ManyToManyField(db_table='ItemToppingJoin', to='Pizza.topping'),
        ),
    ]
