# Generated by Django 5.0.4 on 2024-05-31 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe_app', '0005_alter_producto_imagen_alter_venta_fecha'),
    ]

    operations = [
        migrations.CreateModel(
            name='Descuento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_descuento', models.CharField(max_length=90)),
                ('desc', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]