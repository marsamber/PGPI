# Generated by Django 4.1.3 on 2022-12-11 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_merge_20221209_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='estado_pedido',
            field=models.CharField(choices=[('No pagado', 'no_pagado'), ('Comprado', 'comprado'), ('Enviado', 'enviado'), ('Recogido', 'recogido')], default='No pagado', max_length=256),
        ),
    ]