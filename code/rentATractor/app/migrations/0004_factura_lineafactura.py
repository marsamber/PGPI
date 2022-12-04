# Generated by Django 4.1.3 on 2022-12-01 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_pedido_pago_contrareembolso_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('pedido', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.pedido')),
                ('fecha', models.DateField()),
                ('nombre_cliente', models.CharField(max_length=256)),
                ('apellidos_cliente', models.CharField(max_length=256)),
                ('direccion', models.CharField(max_length=256)),
                ('dni', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='LineaFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=256)),
                ('iva', models.FloatField()),
                ('precio_sin_iva', models.FloatField()),
                ('descuento', models.FloatField(default=0.0)),
                ('cantidad', models.IntegerField()),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.factura')),
            ],
        ),
    ]