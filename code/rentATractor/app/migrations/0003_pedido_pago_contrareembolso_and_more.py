# Generated by Django 4.1.3 on 2022-11-30 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_maquina_sugerido'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='pago_contrareembolso',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pedido',
            name='recogida_en_tienda',
            field=models.BooleanField(default=False),
        ),
    ]
