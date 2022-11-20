from django.contrib import admin
from app.models import Maquina, Cliente, Pedido, Tarjeta, ClienteRegistrado, Opinion, Reclamacion, Descuento, Contiene

admin.site.register(Maquina)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Tarjeta)
admin.site.register(ClienteRegistrado)
admin.site.register(Opinion)
admin.site.register(Reclamacion)
admin.site.register(Descuento)
admin.site.register(Contiene)