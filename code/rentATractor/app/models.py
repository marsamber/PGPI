from django.db import models
from enum import Enum
from django.contrib.auth.models import User

class TipoMaquina(Enum):
    manipulacion_cargas = 'Manipulacion de cargas'
    movimiento_tierras = 'Movimiento de tierras'
    excavadoras = 'excavadoras'
    plataformas_elevadoras = 'Plataformas elevadoras'
    andamios = 'Andamios'
    gruas = 'Gruas'
    maquinaria_hormigon = 'Maquinaria de hormigon'
    herramientas_mano = 'Herramientas de mano'
    apisonadoras = 'Apisonadoras'
    varios = 'Varios'

    @classmethod
    def choices(cls):
        return [(key.value, key.name)for key in cls]

class EstadoPedido(Enum):
    comprado = 'Comprado'
    enviado = 'Enviado'
    recogido = 'Recogido'

    @classmethod
    def choices(cls):
        return [(key.value, key.name)for key in cls]

class Maquina(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=64)
    descripcion = models.CharField(max_length=256)
    precio = models.FloatField()
    stock = models.IntegerField()
    marca = models.CharField(max_length=64)
    fabricante = models.CharField(max_length=64)
    dimensiones = models.CharField(max_length=256)
    imagen = models.CharField(max_length=256)
    tipo_maquina = models.CharField(choices=TipoMaquina.choices(), default=TipoMaquina.varios, max_length=256)
    descuento = models.FloatField(default=0.0)
    
class Cliente(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=64)
    apellidos = models.CharField(max_length=64)
    dni = models.CharField(max_length=32)
    fecha_nacimiento = models.DateField()
    correo = models.CharField(max_length=64)

class ClienteRegistrado(models.Model):
    cliente = models.OneToOneField('Cliente', primary_key=True, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=256)
    gusta = models.ManyToManyField('Maquina')

class Pedido(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha_pedido = models.DateField()
    direccion_envio = models.CharField(max_length=256)
    direccion_facturacion = models.CharField(max_length=256)
    estado_pedido = models.CharField(choices=EstadoPedido.choices(), default=EstadoPedido.comprado, max_length=256)
    cliente = models.ForeignKey('Cliente',on_delete=models.CASCADE)
    maquina = models.ManyToManyField('Maquina')
    tarjeta = models.ForeignKey('Tarjeta',null=True, on_delete=models.SET_NULL)

class Tarjeta(models.Model):
    titular = models.CharField(max_length=256)
    numero = models.CharField(max_length=256)
    codigo = models.CharField(max_length=256)
    fecha_validez = models.DateField()
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)

class Opinion(models.Model):
    cuerpo = models.CharField(max_length=256)
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    maquina = models.ForeignKey('Maquina', on_delete=models.CASCADE)

class Reclamacion(models.Model):
    cuerpo = models.CharField(max_length=256)
    pedido = models.ForeignKey('Pedido',on_delete=models.CASCADE)
    maquina = models.ForeignKey('Maquina',on_delete=models.CASCADE)

class Contiene(models.Model):
    cantidad = models.IntegerField()
    pedido = models.ForeignKey('Pedido',on_delete=models.CASCADE)
    maquina = models.ForeignKey('Maquina',on_delete=models.CASCADE)

class EnCesta(models.Model):
    maquina = models.ForeignKey("Maquina", on_delete=models.CASCADE)
    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE)
    cantidad = models.IntegerField()