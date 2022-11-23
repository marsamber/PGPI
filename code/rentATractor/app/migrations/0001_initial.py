# Generated by Django 4.1.3 on 2022-11-22 07:38

import app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=64)),
                ('apellidos', models.CharField(max_length=64)),
                ('dni', models.CharField(max_length=32)),
                ('fecha_nacimiento', models.DateField()),
                ('correo', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Maquina',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=64)),
                ('descripcion', models.CharField(max_length=256)),
                ('precio', models.FloatField()),
                ('stock', models.IntegerField()),
                ('marca', models.CharField(max_length=64)),
                ('fabricante', models.CharField(max_length=64)),
                ('dimensiones', models.CharField(max_length=256)),
                ('imagen', models.CharField(max_length=256)),
                ('tipo_maquina', models.CharField(choices=[('Manipulacion de cargas', 'manipulacion_cargas'), ('Movimiento de tierras', 'movimiento_tierras'), ('excavadoras', 'excavadoras'), ('Plataformas elevadoras', 'plataformas_elevadoras'), ('Andamios', 'andamios'), ('Gruas', 'gruas'), ('Maquinaria de hormigon', 'maquinaria_hormigon'), ('Herramientas de mano', 'herramientas_mano'), ('Apisonadoras', 'apisonadoras'), ('Varios', 'varios')], default=app.models.TipoMaquina['varios'], max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('fecha_pedido', models.DateField()),
                ('direccion_envio', models.CharField(max_length=256)),
                ('direccion_facturacion', models.CharField(max_length=256)),
                ('estado_pedido', models.CharField(choices=[('Comprado', 'comprado'), ('Enviado', 'enviado'), ('Recogido', 'recogido')], default=app.models.EstadoPedido['comprado'], max_length=256)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cliente')),
                ('maquina', models.ManyToManyField(to='app.maquina')),
            ],
        ),
        migrations.CreateModel(
            name='Tarjeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titular', models.CharField(max_length=256)),
                ('numero', models.CharField(max_length=256)),
                ('codigo', models.CharField(max_length=256)),
                ('fecha_validez', models.DateField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reclamacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuerpo', models.CharField(max_length=256)),
                ('maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.maquina')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.pedido')),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='tarjeta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.tarjeta'),
        ),
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuerpo', models.CharField(max_length=256)),
                ('maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.maquina')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.pedido')),
            ],
        ),
        migrations.CreateModel(
            name='Contiene',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('maquina', models.ManyToManyField(to='app.maquina')),
                ('pedido', models.ManyToManyField(to='app.pedido')),
            ],
        ),
        migrations.CreateModel(
            name='ClienteRegistrado',
            fields=[
                ('cliente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.cliente')),
                ('direccion', models.CharField(max_length=256)),
                ('gusta', models.ManyToManyField(to='app.maquina')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
