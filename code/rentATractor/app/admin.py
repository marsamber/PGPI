from django.contrib import admin
from app.models import Maquina, Cliente, Pedido, Tarjeta, ClienteRegistrado, Opinion, Reclamacion, Contiene, EnCesta

admin.site.register(Maquina)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Tarjeta)
admin.site.register(ClienteRegistrado)
admin.site.register(Opinion)
admin.site.register(Reclamacion)
admin.site.register(Contiene)
admin.site.register(EnCesta)