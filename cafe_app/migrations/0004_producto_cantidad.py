# Generated by Django 5.0.4 on 2024-05-24 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe_app', '0003_remove_producto_cantidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='cantidad',
            field=models.IntegerField(null=True),
        ),
    ]
