from django.contrib import admin
from app.models import Maquina, Cliente, Pedido, Tarjeta, ClienteRegistrado, Opinion, Reclamacion, Contiene, EnCesta, Factura
from django.utils.html import mark_safe

class MaquinaAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre", "marca", "precio", "stock", "tipo_maquina", "descuento", "sugerido"]
    list_editable = ["precio", "stock", "tipo_maquina"]
    search_fields = ["nombre"]
    search_help_text = 'Búsqueda por el "nombre" de la máquina'
    list_filter = ["marca", "precio", "tipo_maquina", "sugerido"]
    list_per_page = 10

class ClienteAdmin(admin.ModelAdmin):
    list_display = ["dni", "nombre", "apellidos", "correo"]
    list_editable = ["correo"]
    search_fields = ["nombre", "apellidos", "dni", "correo"]
    search_help_text = 'Búsqueda por el "nombre", "apellidos", "DNI" o "email" del cliente (no registrado).'
    list_per_page = 10

class PedidoAdmin(admin.ModelAdmin):
    list_display = ["id", "fecha_pedido", "estado_pedido", "get_cliente", "get_maquina", "pago_contrareembolso", "recogida_en_tienda"]
    list_editable = ["estado_pedido"]
    search_fields = ["id", "estado_pedido", "cliente__dni"]
    search_help_text = 'Búsqueda por el "id", "cliente" o "estado" del pedido.'
    list_filter = ["estado_pedido"]
    list_per_page = 10

    def get_cliente(self, obj):
        return obj.cliente.dni
    get_cliente.short_description = 'cliente'
    get_cliente.admin_order_field = 'cliente'

    def get_maquina(self, obj):
        to_return = '<ul>'
        to_return += '\n'.join('<li>{}</li>'.format(maq_nombre) for maq_nombre in obj.maquina.values_list('nombre', flat=True))
        to_return += '</ul>'
        return mark_safe(to_return)
    get_maquina.short_description = 'maquinas'
    get_maquina.admin_order_field = 'maquinas'

class TarjetaAdmin(admin.ModelAdmin):
    list_display = ["titular", "numero", "codigo", "fecha_validez", "get_usuario"]
    list_editable = ["codigo"]
    search_fields = ["titular", "numero", "codigo", "uuario__username"]
    search_help_text = 'Búsqueda por "titular", "número" o "código" de la tarjeta. También, puede buscar por el "nombre de usuario".'
    list_per_page = 10

    def get_usuario(self, obj):
        return obj.usuario
    get_usuario.short_description = 'usuario'
    get_usuario.admin_order_field = 'usuario'

class ClienteRegistradoAdmin(admin.ModelAdmin):
    list_display = ["get_cliente", "get_user", "direccion", "get_gusta"]
    search_fields = ["cliente__dni", "user__username"]
    search_help_text = 'Búsqueda por el "DNI" del cliente del pedido, o "nombre de usuario".'
    list_per_page = 10

    def get_cliente(self, obj):
        return obj.cliente.dni
    get_cliente.short_description = 'cliente'
    get_cliente.admin_order_field = 'cliente'

    def get_gusta(self, obj):
        to_return = '<ul>'
        to_return += '\n'.join('<li>{}</li>'.format(maq_nombre) for maq_nombre in obj.gusta.values_list('nombre', flat=True))
        to_return += '</ul>'
        return mark_safe(to_return)
    get_gusta.short_description = 'favoritos'
    get_gusta.admin_order_field = 'favoritos'

    def get_user(self, obj):
        return obj.user
    get_user.short_description = 'usuario'
    get_user.admin_order_field = 'usuario'

class OpinionAdmin(admin.ModelAdmin):
    list_display = ["cuerpo", "get_pedido", "get_maquina"]
    search_fields = ["pedido__id", "maquina__nombre"]
    search_help_text = 'Búsqueda por el "id" del pedido o "nombre" de la maquina.'
    list_filter = ["pedido__id"]
    list_per_page = 10

    def get_pedido(self, obj):
        return obj.pedido.id
    get_pedido.short_description = 'pedido'
    get_pedido.admin_order_field = 'pedido'

    def get_maquina(self, obj):
        return obj.maquina.nombre
    get_maquina.short_description = 'maquina'
    get_maquina.admin_order_field = 'maquina'

class ReclamacionAdmin(admin.ModelAdmin):
    list_display = ["cuerpo", "get_pedido", "get_maquina"]
    search_fields = ["pedido__id", "maquina__nombre"]
    search_help_text = 'Búsqueda por el "id" del pedido o "nombre" de la maquina.'
    list_filter = ["pedido__id"]
    list_per_page = 10

    def get_pedido(self, obj):
        return obj.pedido.id
    get_pedido.short_description = 'pedido'
    get_pedido.admin_order_field = 'pedido'

    def get_maquina(self, obj):
        return obj.maquina.nombre
    get_maquina.short_description = 'maquina'
    get_maquina.admin_order_field = 'maquina'

class ContieneAdmin(admin.ModelAdmin):
    list_display = ["id", "cantidad", "get_pedido", "get_maquina"]
    list_editable = ["cantidad"]
    search_fields = ["pedido__id", "maquina__nombre"]
    search_help_text = 'Búsqueda por el "id" del pedido o "nombre" de la maquina.'
    list_filter = ["pedido__id"]
    list_per_page = 10

    def get_pedido(self, obj):
        return obj.pedido.id
    get_pedido.short_description = 'pedido'
    get_pedido.admin_order_field = 'pedido'

    def get_maquina(self, obj):
        return obj.maquina.nombre
    get_maquina.short_description = 'maquina'
    get_maquina.admin_order_field = 'maquina'

class EnCestaAdmin(admin.ModelAdmin):
    list_display = ["id", "cantidad", "get_cliente", "get_maquina"]
    list_editable = ["cantidad"]
    search_fields = ["maquina__id", "cliente__dni"]
    search_help_text = 'Búsqueda por el "DNI" del cliente o "nombre" de la maquina.'
    list_per_page = 10

    def get_maquina(self, obj):
        return obj.maquina.id
    get_maquina.short_description = 'maquina'
    get_maquina.admin_order_field = 'maquina'

    def get_cliente(self, obj):
        return obj.cliente.dni
    get_cliente.short_description = 'cliente'
    get_cliente.admin_order_field = 'cliente'

admin.site.register(Maquina, MaquinaAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Tarjeta, TarjetaAdmin)
admin.site.register(ClienteRegistrado, ClienteRegistradoAdmin)
admin.site.register(Opinion, OpinionAdmin)
admin.site.register(Reclamacion, ReclamacionAdmin)
admin.site.register(Contiene, ContieneAdmin)
admin.site.register(EnCesta, EnCestaAdmin)
admin.site.register(Factura)