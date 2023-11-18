# Generated by Django 4.2.5 on 2023-11-18 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0007_remove_contacto_avisos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1)),
                ('precio_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('libro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.libro')),
            ],
        ),
    ]