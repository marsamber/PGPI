# Generated by Django 4.1.3 on 2022-12-11 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_pedido_estado_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='maquina',
            name='sugerencias',
            field=models.ManyToManyField(null=True, to='app.maquina'),
        ),
    ]
