# Generated by Django 4.2.5 on 2023-11-29 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0009_autor_editorial_rename_precio_libro_precio_venta_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
    ]
