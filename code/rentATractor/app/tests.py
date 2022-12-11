import datetime
from django.test import TestCase
from app.models import Cliente, ClienteRegistrado, Contiene, EnCesta, Factura, LineaFactura, Maquina, Opinion, Pedido, Reclamacion
from django.contrib.auth.models import User

class ModelsTestCase(TestCase):
    # Configura las pruebas
    def setUp(self):
        # Crea dos maquinas de prueba
        Maquina.objects.create(
            id=1,
            nombre='Maquina de prueba',
            descripcion='Descripcion de prueba',
            precio = 100.0,
            stock = 10,
            marca = 'Marca de prueba',
            fabricante = 'Fabricante de prueba',
            dimensiones = 'Dimensiones de prueba',
            imagen = 'Imagen de prueba',
            tipo_maquina = 'Varios',
            descuento = 0.0,
            sugerido = False
        )
        Maquina.objects.create(
            id=2,
            nombre='Maquina de prueba',
            descripcion='Descripcion de prueba',
            precio = 100.0,
            stock = 10,
            marca = 'Marca de prueba',
            fabricante = 'Fabricante de prueba',
            dimensiones = 'Dimensiones de prueba',
            imagen = 'Imagen de prueba',
            tipo_maquina = 'Varios',
            descuento = 0.0,
            sugerido = False
        )

        # Crea tres usuarios de prueba
        User.objects.create(
            id=2,
            username='Usuario de prueba2',
            password='Contraseña de prueba',
            email='Correo de prueba',
            first_name='Nombre de prueba',
            last_name='Apellidos de prueba',
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login='2021-01-01',
            date_joined='2021-01-01'
        )
        User.objects.create(
            id=3,
            username='Usuario de prueba3',
            password='Contraseña de prueba',
            email='Correo de prueba',
            first_name='Nombre de prueba',
            last_name='Apellidos de prueba',
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login='2021-01-01',
            date_joined='2021-01-01'
        )
        User.objects.create(
            id=4,
            username='Usuario de prueba4',
            password='Contraseña de prueba',
            email='Correo de prueba',
            first_name='Nombre de prueba',
            last_name='Apellidos de prueba',
            is_staff=False,
            is_active=True,
            is_superuser=False, 
            last_login='2021-01-01',
            date_joined='2021-01-01'
        )

        #Crea tres clientes de prueba
        Cliente.objects.create(
            id=1,
            nombre='Cliente de prueba',
            apellidos='Apellidos de prueba',
            dni='DNI de prueba',
            fecha_nacimiento='1992-01-01',
            correo='Correo de prueba',
        )
        Cliente.objects.create(
            id=2,
            nombre='Cliente de prueba',
            apellidos='Apellidos de prueba',
            dni='DNI de prueba',
            fecha_nacimiento='1992-01-01',
            correo='Correo de prueba',
        )
        Cliente.objects.create(
            id=3,
            nombre='Cliente de prueba',
            apellidos='Apellidos de prueba',
            dni='DNI de prueba',
            fecha_nacimiento='1992-01-01',
            correo='Correo de prueba',
        )

        #Crea dos clientes registrados de prueba
        clienteRegistrado1 = ClienteRegistrado.objects.create(
            cliente = Cliente.objects.get(id=1),
            user = User.objects.get(id=2),
            direccion = 'Direccion de prueba'
        )
        clienteRegistrado1.gusta.set(Maquina.objects.filter(id=1))
        clienteRegistrado1.save()

        clienteRegistrado2 = ClienteRegistrado.objects.create(
            cliente = Cliente.objects.get(id=2),
            user = User.objects.get(id=3),
            direccion = 'Direccion de prueba'
        )
        clienteRegistrado2.gusta.set(Maquina.objects.filter(id=2))
        clienteRegistrado2.save()

        #Crea tres pedidos de prueba
        pedido1 = Pedido.objects.create(
            id=1,
            fecha_pedido='2021-01-01',
            direccion_envio='Direccion de envio de prueba',
            direccion_facturacion='Direccion de facturacion de prueba',
            estado_pedido='no_pagado',
            cliente=Cliente.objects.get(id=1),
            pago_contrareembolso=False,
            recogida_en_tienda=False
        )
        pedido1.maquina.set(Maquina.objects.filter(id=1))
        pedido2 = Pedido.objects.create(
            id=2,
            fecha_pedido='2021-01-01',
            direccion_envio='Direccion de envio de prueba',
            direccion_facturacion='Direccion de facturacion de prueba',
            estado_pedido='no_pagado',
            cliente=Cliente.objects.get(id=2),
            pago_contrareembolso=False,
            recogida_en_tienda=False
        )
        pedido2.maquina.set(Maquina.objects.filter(id=2))
        pedido3 = Pedido.objects.create(
            id=3,
            fecha_pedido='2021-01-01',
            direccion_envio='Direccion de envio de prueba',
            direccion_facturacion='Direccion de facturacion de prueba',
            estado_pedido='no_pagado',
            cliente=Cliente.objects.get(id=3),
            pago_contrareembolso=False,
            recogida_en_tienda=False
        )
        pedido3.maquina.set(Maquina.objects.filter(id=3))

        #Crea dos opiniones de prueba
        Opinion.objects.create(
            id=1,
            cuerpo='Cuerpo de prueba',
            pedido = Pedido.objects.get(id=1),
            maquina = Maquina.objects.get(id=1)
        )
        Opinion.objects.create(
            id=2,
            cuerpo='Cuerpo de prueba',
            pedido = Pedido.objects.get(id=2),
            maquina = Maquina.objects.get(id=2)
        )

        #Crea dos reclamaciones de prueba
        Reclamacion.objects.create(
            id=1,
            cuerpo='Cuerpo de prueba',
            pedido = Pedido.objects.get(id=1),
            maquina = Maquina.objects.get(id=1)
        )
        Reclamacion.objects.create(
            id=2,
            cuerpo='Cuerpo de prueba',
            pedido = Pedido.objects.get(id=2),
            maquina = Maquina.objects.get(id=2)
        )

        #Crea dos contiene de prueba
        Contiene.objects.create(
            id=1,
            pedido = Pedido.objects.get(id=1),
            maquina = Maquina.objects.get(id=1),
            cantidad = 1
        )
        Contiene.objects.create(
            id=2,
            pedido = Pedido.objects.get(id=2),
            maquina = Maquina.objects.get(id=2),
            cantidad = 1
        )

        #Crea dos elementos en cesta de prueba
        EnCesta.objects.create(
            id=1,
            maquina=Maquina.objects.get(id=1),
            cliente=Cliente.objects.get(id=1),
            cantidad=1
        )
        EnCesta.objects.create(
            id=2,
            maquina=Maquina.objects.get(id=2),
            cliente=Cliente.objects.get(id=2),
            cantidad=1
        )

        #Crea dos facturas de prueba
        Factura.objects.create(
            fecha='2021-01-01',
            pedido=Pedido.objects.get(id=1),
            nombre_cliente='Nombre de prueba',
            apellidos_cliente='Apellidos de prueba',
            direccion='Direccion de prueba',
            dni='12345678A'
        )
        Factura.objects.create(
            fecha='2021-01-01',
            pedido=Pedido.objects.get(id=2),
            nombre_cliente='Nombre de prueba',
            apellidos_cliente='Apellidos de prueba',
            direccion='Direccion de prueba',
            dni='12345678A'
        )

        #Crea dos lineas de factura de prueba
        LineaFactura.objects.create(
            id=1,
            factura=Factura.objects.get(pedido__id=1),
            nombre = 'Nombre de prueba',
            iva = 21,
            precio_sin_iva = 100,
            descuento = 0,
            cantidad = 1
        )
        LineaFactura.objects.create(
            id=2,
            factura=Factura.objects.get(pedido__id=2),
            nombre = 'Nombre de prueba',
            iva = 21,
            precio_sin_iva = 100,
            descuento = 0,
            cantidad = 1
        )

    # Desconfigura las pruebas
    def tearDown(self):
        # Borra las maquinas de prueba
        Maquina.objects.all().delete()
        # Borra los clientes de prueba
        Cliente.objects.all().delete()
        # Borra los clientes registrados de prueba
        ClienteRegistrado.objects.all().delete()
        # Borra los pedidos de prueba
        Pedido.objects.all().delete()
        # Borra las opiniones de prueba
        Opinion.objects.all().delete()
        # Borra las reclamaciones de prueba
        Reclamacion.objects.all().delete()
        # Borra los contiene de prueba
        Contiene.objects.all().delete()
        # Borra los elementos en cesta de prueba
        EnCesta.objects.all().delete()
        # Borra las facturas de prueba
        Factura.objects.all().delete()
        # Borra las lineas de factura de prueba
        LineaFactura.objects.all().delete()

    # Tests de la clase Maquina
    # Comprueba que se pueden obtener las maquinas de la base de datos
    def test_maquina_retrieve(self):
        # Obtiene una maquina de la base de datos
        maquina = Maquina.objects.get(id=1)
        # Comprueba que la maquina se ha obtenido correctamente
        self.assertEqual(maquina.nombre, 'Maquina de prueba')
        self.assertEqual(maquina.descripcion, 'Descripcion de prueba')
        self.assertEqual(maquina.precio, 100.0)
        self.assertEqual(maquina.stock, 10)
        self.assertEqual(maquina.marca, 'Marca de prueba')
        self.assertEqual(maquina.fabricante, 'Fabricante de prueba')
        self.assertEqual(maquina.dimensiones, 'Dimensiones de prueba')
        self.assertEqual(maquina.imagen, 'Imagen de prueba')
        self.assertEqual(maquina.tipo_maquina, 'Varios')
        self.assertEqual(maquina.descuento, 0.0)
        self.assertEqual(maquina.sugerido, False)

    # Comprueba que se pueden crear maquinas
    def test_maquina_create(self):
        # Crea una maquina con los datos de prueba
        maquina = Maquina.objects.create(
            id=3,
            nombre='Maquina de prueba',
            descripcion='Descripcion de prueba',
            precio = 100.0,
            stock = 10,
            marca = 'Marca de prueba',
            fabricante = 'Fabricante de prueba',
            dimensiones = 'Dimensiones de prueba',
            imagen = 'Imagen de prueba',
            tipo_maquina = 'Varios',
            descuento = 0.0,
            sugerido = False
        )
        # Comprueba que la maquina se ha creado correctamente
        self.assertEqual(maquina.nombre, 'Maquina de prueba')
        self.assertEqual(maquina.descripcion, 'Descripcion de prueba')
        self.assertEqual(maquina.precio, 100.0)
        self.assertEqual(maquina.stock, 10)
        self.assertEqual(maquina.marca, 'Marca de prueba')
        self.assertEqual(maquina.fabricante, 'Fabricante de prueba')
        self.assertEqual(maquina.dimensiones, 'Dimensiones de prueba')
        self.assertEqual(maquina.imagen, 'Imagen de prueba')
        self.assertEqual(maquina.tipo_maquina, 'Varios')
        self.assertEqual(maquina.descuento, 0.0)
        self.assertEqual(maquina.sugerido, False)
        # Borra la maquina de prueba
        maquina.delete()
    
    # Comprueba que se pueden actualizar maquinas
    def test_maquina_update(self):
        # Obtiene una maquina de la base de datos
        maquina = Maquina.objects.get(id=1)
        # Actualiza la maquina
        maquina.nombre = 'Maquina de prueba actualizada'
        maquina.descripcion = 'Descripcion de prueba actualizada'
        maquina.precio = 200.0
        maquina.stock = 20
        maquina.marca = 'Marca de prueba actualizada'
        maquina.fabricante = 'Fabricante de prueba actualizada'
        maquina.dimensiones = 'Dimensiones de prueba actualizada'
        maquina.imagen = 'Imagen de prueba actualizada'
        maquina.tipo_maquina = 'Varios'
        maquina.descuento = 0.0
        maquina.sugerido = False
        maquina.save()
        # Comprueba que la maquina se ha actualizado correctamente
        self.assertEqual(maquina.nombre, 'Maquina de prueba actualizada')
        self.assertEqual(maquina.descripcion, 'Descripcion de prueba actualizada')
        self.assertEqual(maquina.precio, 200.0)
        self.assertEqual(maquina.stock, 20)
        self.assertEqual(maquina.marca, 'Marca de prueba actualizada')
        self.assertEqual(maquina.fabricante, 'Fabricante de prueba actualizada')
        self.assertEqual(maquina.dimensiones, 'Dimensiones de prueba actualizada')
        self.assertEqual(maquina.imagen, 'Imagen de prueba actualizada')
        self.assertEqual(maquina.tipo_maquina, 'Varios')
        self.assertEqual(maquina.descuento, 0.0)
        self.assertEqual(maquina.sugerido, False)

    # Comprueba que se pueden borrar maquinas
    def test_maquina_delete(self):
        # Obtiene una maquina de la base de datos
        maquina = Maquina.objects.get(id=2)
        # Borra la maquina
        maquina.delete()
        # Comprueba que la maquina se ha borrado correctamente
        self.assertRaises(Maquina.DoesNotExist, Maquina.objects.get, id=2)

    # Tests de la clase Cliente
    # Comprueba que se pueden obtener los clientes de la base de datos
    def test_cliente_retrieve(self):
        # Obtiene un cliente de la base de datos
        cliente = Cliente.objects.get(id=1)
        # Comprueba que el cliente se ha obtenido correctamente
        self.assertEqual(cliente.nombre, 'Cliente de prueba')
        self.assertEqual(cliente.apellidos, 'Apellidos de prueba')
        self.assertEqual(cliente.dni, 'DNI de prueba')
        self.assertEqual(cliente.fecha_nacimiento, datetime.datetime.strptime('1992-01-01', '%Y-%m-%d').date())
        self.assertEqual(cliente.correo, 'Correo de prueba')
    
    # Comprueba que se pueden crear clientes
    def test_cliente_create(self):
        # Crea un cliente con los datos de prueba
        cliente = Cliente.objects.create(
            id=4,
            nombre='Cliente de prueba',
            apellidos='Apellidos de prueba',
            dni = 'DNI de prueba',
            fecha_nacimiento = '1992-01-01',
            correo = 'Correo de prueba'
        )
        # Comprueba que el cliente se ha creado correctamente
        self.assertEqual(cliente.nombre, 'Cliente de prueba')
        self.assertEqual(cliente.apellidos, 'Apellidos de prueba')
        self.assertEqual(cliente.dni, 'DNI de prueba')
        self.assertEqual(cliente.fecha_nacimiento, '1992-01-01')
        self.assertEqual(cliente.correo, 'Correo de prueba')
        # Borra el cliente de prueba
        cliente.delete()

    # Comprueba que se pueden actualizar clientes
    def test_cliente_update(self):
        # Obtiene un cliente de la base de datos
        cliente = Cliente.objects.get(id=1)
        # Actualiza el cliente
        cliente.nombre = 'Cliente de prueba actualizado'
        cliente.apellidos = 'Apellidos de prueba actualizados'
        cliente.dni = 'DNI de prueba actualizado'
        cliente.fecha_nacimiento = '1992-01-02'
        cliente.correo = 'Correo de prueba actualizado'
        cliente.save()
        # Comprueba que el cliente se ha actualizado correctamente
        self.assertEqual(cliente.nombre, 'Cliente de prueba actualizado')
        self.assertEqual(cliente.apellidos, 'Apellidos de prueba actualizados')
        self.assertEqual(cliente.dni, 'DNI de prueba actualizado')
        self.assertEqual(cliente.fecha_nacimiento, '1992-01-02')
        self.assertEqual(cliente.correo, 'Correo de prueba actualizado')

    # Comprueba que se pueden borrar clientes
    def test_cliente_delete(self):
        # Obtiene un cliente de la base de datos
        cliente = Cliente.objects.get(id=2)
        # Borra el cliente
        cliente.delete()
        # Comprueba que el cliente se ha borrado correctamente
        self.assertRaises(Cliente.DoesNotExist, Cliente.objects.get, id=2)

    # Tests de la clase Cliente Registrado
    # Comprueba que se pueden obtener los clientes registrados de la base de datos
    def test_cliente_registrado_retrieve(self):
        # Obtiene un cliente registrado de la base de datos
        cliente_registrado = ClienteRegistrado.objects.get(cliente__id = 1)
        # Comprueba que el cliente registrado se ha obtenido correctamente
        self.assertEqual(cliente_registrado.cliente, Cliente.objects.get(id=1))
        self.assertEqual(cliente_registrado.user, User.objects.get(id=2))
        self.assertEqual(cliente_registrado.direccion, 'Direccion de prueba')

    # Comprueba que se pueden crear clientes registrados
    def test_cliente_registrado_create(self):
        # Crea un cliente registrado con los datos de prueba
        cliente_registrado = ClienteRegistrado.objects.create(
            cliente = Cliente.objects.get(id=3),
            user = User.objects.get(id=4),
            direccion = 'Direccion de prueba'
        )
        cliente_registrado.gusta.set(Maquina.objects.filter(id=1))
        # Comprueba que el cliente registrado se ha creado correctamente
        self.assertEqual(cliente_registrado.cliente, Cliente.objects.get(id=3))
        self.assertEqual(cliente_registrado.user, User.objects.get(id=4))
        self.assertEqual(cliente_registrado.direccion, 'Direccion de prueba')
        # Borra el cliente registrado de prueba
        cliente_registrado.delete()

    # Comprueba que se pueden actualizar clientes registrados
    def test_cliente_registrado_update(self):
        # Obtiene un cliente registrado de la base de datos
        cliente_registrado = ClienteRegistrado.objects.get(cliente__id=1)
        # Actualiza el cliente registrado
        cliente_registrado.direccion = 'Direccion de prueba actualizada'
        cliente_registrado.save()
        # Comprueba que el cliente registrado se ha actualizado correctamente
        self.assertEqual(cliente_registrado.direccion, 'Direccion de prueba actualizada')

    # Comprueba que se pueden borrar clientes registrados
    def test_cliente_registrado_delete(self):
        # Obtiene un cliente registrado de la base de datos
        cliente_registrado = ClienteRegistrado.objects.get(cliente__id=2)
        # Borra el cliente registrado
        cliente_registrado.delete()
        # Comprueba que el cliente registrado se ha borrado correctamente
        self.assertRaises(ClienteRegistrado.DoesNotExist, ClienteRegistrado.objects.get, cliente__id=2)

    # Tests de la clase Pedido
    # Comprueba que se pueden obtener los pedidos de la base de datos
    def test_pedido_retrieve(self):
        # Obtiene un pedido de la base de datos
        pedido = Pedido.objects.get(id=1)
        # Comprueba que el pedido se ha obtenido correctamente
        self.assertEqual(pedido.fecha_pedido, datetime.datetime.strptime('2021-01-01', '%Y-%m-%d').date())
        self.assertEqual(pedido.direccion_envio, 'Direccion de envio de prueba')
        self.assertEqual(pedido.direccion_facturacion, 'Direccion de facturacion de prueba')
        self.assertEqual(pedido.estado_pedido, 'no_pagado')
        self.assertEqual(pedido.cliente, Cliente.objects.get(id=1))
        self.assertEqual(pedido.pago_contrareembolso, False)
        self.assertEqual(pedido.recogida_en_tienda, False)

    # Comprueba que se pueden crear pedidos
    def test_pedido_create(self):
        # Crea un pedido con los datos de prueba
        pedido = Pedido.objects.create(
            id = 4,
            fecha_pedido = '2020-01-01',
            direccion_envio = 'Direccion de prueba',
            direccion_facturacion = 'Direccion de prueba',
            estado_pedido = 'no_pagado',
            cliente = Cliente.objects.get(id=1),
            pago_contrareembolso = False,
            recogida_en_tienda = False
        )
        # Comprueba que el pedido se ha creado correctamente
        self.assertEqual(pedido.fecha_pedido, '2020-01-01')
        self.assertEqual(pedido.direccion_envio, 'Direccion de prueba')
        self.assertEqual(pedido.direccion_facturacion, 'Direccion de prueba')
        self.assertEqual(pedido.estado_pedido, 'no_pagado')
        self.assertEqual(pedido.cliente, Cliente.objects.get(id=1))
        self.assertEqual(pedido.pago_contrareembolso, False)
        self.assertEqual(pedido.recogida_en_tienda, False)
        # Borra el pedido de prueba
        pedido.delete()

    # Comprueba que se pueden actualizar pedidos
    def test_pedido_update(self):
        # Obtiene un pedido de la base de datos
        pedido = Pedido.objects.get(id=1)
        # Actualiza el pedido
        pedido.estado_pedido = 'pagado'
        pedido.save()
        # Comprueba que el pedido se ha actualizado correctamente
        self.assertEqual(pedido.estado_pedido, 'pagado')

    # Comprueba que se pueden borrar pedidos
    def test_pedido_delete(self):
        # Obtiene un pedido de la base de datos
        pedido = Pedido.objects.get(id=1)
        # Borra el pedido
        pedido.delete()
        # Comprueba que el pedido se ha borrado correctamente
        self.assertRaises(Pedido.DoesNotExist, Pedido.objects.get, id=1)

    # Tests de la clase Opinion
    # Comprueba que se pueden obtener las opiniones de la base de datos
    def test_opinion_retrieve(self):
        # Obtiene una opinion de la base de datos
        opinion = Opinion.objects.get(id=1)
        # Comprueba que la opinion se ha obtenido correctamente
        self.assertEqual(opinion.cuerpo, 'Cuerpo de prueba')
        self.assertEqual(opinion.pedido, Pedido.objects.get(id=1))
        self.assertEqual(opinion.maquina, Maquina.objects.get(id=1))

    # Comprueba que se pueden crear opiniones
    def test_opinion_create(self):
        # Crea una opinion con los datos de prueba
        opinion = Opinion.objects.create(
            id = 3,
            cuerpo = 'Cuerpo de prueba',
            pedido = Pedido.objects.get(id=1),
            maquina = Maquina.objects.get(id=1)
        )
        # Comprueba que la opinion se ha creado correctamente
        self.assertEqual(opinion.cuerpo, 'Cuerpo de prueba')
        self.assertEqual(opinion.pedido, Pedido.objects.get(id=1))
        self.assertEqual(opinion.maquina, Maquina.objects.get(id=1))
        # Borra la opinion de prueba
        opinion.delete()

    # Comprueba que se pueden actualizar opiniones
    def test_opinion_update(self):
        # Obtiene una opinion de la base de datos
        opinion = Opinion.objects.get(id=1)
        # Actualiza la opinion
        opinion.cuerpo = 'Cuerpo de prueba actualizado'
        opinion.save()
        # Comprueba que la opinion se ha actualizado correctamente
        self.assertEqual(opinion.cuerpo, 'Cuerpo de prueba actualizado')

    # Comprueba que se pueden borrar opiniones
    def test_opinion_delete(self):
        # Obtiene una opinion de la base de datos
        opinion = Opinion.objects.get(id=1)
        # Borra la opinion
        opinion.delete()
        # Comprueba que la opinion se ha borrado correctamente
        self.assertRaises(Opinion.DoesNotExist, Opinion.objects.get, id=1)

    # Tests de la clase Reclamacion
    # Comprueba que se pueden obtener las reclamaciones de la base de datos
    def test_reclamacion_retrieve(self):
        # Obtiene una reclamacion de la base de datos
        reclamacion = Reclamacion.objects.get(id=1)
        # Comprueba que la reclamacion se ha obtenido correctamente
        self.assertEqual(reclamacion.cuerpo, 'Cuerpo de prueba')
        self.assertEqual(reclamacion.pedido, Pedido.objects.get(id=1))
        self.assertEqual(reclamacion.maquina, Maquina.objects.get(id=1))

    # Comprueba que se pueden crear reclamaciones
    def test_reclamacion_create(self):
        # Crea una reclamacion con los datos de prueba
        reclamacion = Reclamacion.objects.create(
            id = 3,
            cuerpo = 'Cuerpo de prueba',
            pedido = Pedido.objects.get(id=1),
            maquina = Maquina.objects.get(id=1)
        )
        # Comprueba que la reclamacion se ha creado correctamente
        self.assertEqual(reclamacion.cuerpo, 'Cuerpo de prueba')
        self.assertEqual(reclamacion.pedido, Pedido.objects.get(id=1))
        self.assertEqual(reclamacion.maquina, Maquina.objects.get(id=1))
        # Borra la reclamacion de prueba
        reclamacion.delete()

    # Comprueba que se pueden actualizar reclamaciones
    def test_reclamacion_update(self):
        # Obtiene una reclamacion de la base de datos
        reclamacion = Reclamacion.objects.get(id=1)
        # Actualiza la reclamacion
        reclamacion.cuerpo = 'Cuerpo de prueba actualizado'
        reclamacion.save()
        # Comprueba que la reclamacion se ha actualizado correctamente
        self.assertEqual(reclamacion.cuerpo, 'Cuerpo de prueba actualizado')

    # Comprueba que se pueden borrar reclamaciones
    def test_reclamacion_delete(self):
        # Obtiene una reclamacion de la base de datos
        reclamacion = Reclamacion.objects.get(id=1)
        # Borra la reclamacion
        reclamacion.delete()
        # Comprueba que la reclamacion se ha borrado correctamente
        self.assertRaises(Reclamacion.DoesNotExist, Reclamacion.objects.get, id=1)

    # Tests de la clase Contiene
    # Comprueba que se pueden obtener los contenidos de la base de datos
    def test_contiene_retrieve(self):
        # Obtiene un contenido de la base de datos
        contiene = Contiene.objects.get(id=1)
        # Comprueba que el contenido se ha obtenido correctamente
        self.assertEqual(contiene.pedido, Pedido.objects.get(id=1))
        self.assertEqual(contiene.maquina, Maquina.objects.get(id=1))
        self.assertEqual(contiene.cantidad, 1)

    # Comprueba que se pueden crear contenidos
    def test_contiene_create(self):
        # Crea un contenido con los datos de prueba
        contiene = Contiene.objects.create(
            id = 3,
            pedido = Pedido.objects.get(id=1),
            maquina = Maquina.objects.get(id=1),
            cantidad = 1
        )
        # Comprueba que el contenido se ha creado correctamente
        self.assertEqual(contiene.pedido, Pedido.objects.get(id=1))
        self.assertEqual(contiene.maquina, Maquina.objects.get(id=1))
        self.assertEqual(contiene.cantidad, 1)
        # Borra el contenido de prueba
        contiene.delete()

    # Comprueba que se pueden actualizar contenidos
    def test_contiene_update(self):
        # Obtiene un contenido de la base de datos
        contiene = Contiene.objects.get(id=1)
        # Actualiza el contenido
        contiene.cantidad = 2
        contiene.save()
        # Comprueba que el contenido se ha actualizado correctamente
        self.assertEqual(contiene.cantidad, 2)

    # Comprueba que se pueden borrar contenidos
    def test_contiene_delete(self):
        # Obtiene un contenido de la base de datos
        contiene = Contiene.objects.get(id=1)
        # Borra el contenido
        contiene.delete()
        # Comprueba que el contenido se ha borrado correctamente
        self.assertRaises(Contiene.DoesNotExist, Contiene.objects.get, id=1)

    # Tests de la clase EnCesta
    # Comprueba que se pueden obtener los contenidos de la cesta de la base de datos
    def test_encesta_retrieve(self):
        # Obtiene un contenido de la cesta de la base de datos
        encesta = EnCesta.objects.get(id=1)
        # Comprueba que el contenido se ha obtenido correctamente
        self.assertEqual(encesta.cliente, Cliente.objects.get(id=1))
        self.assertEqual(encesta.maquina, Maquina.objects.get(id=1))
        self.assertEqual(encesta.cantidad, 1)

    # Comprueba que se pueden crear contenidos de la cesta
    def test_encesta_create(self):
        # Crea un contenido de la cesta con los datos de prueba
        encesta = EnCesta.objects.create(
            id = 3,
            cliente = Cliente.objects.get(id=1),
            maquina = Maquina.objects.get(id=1),
            cantidad = 1
        )
        # Comprueba que el contenido se ha creado correctamente
        self.assertEqual(encesta.cliente, Cliente.objects.get(id=1))
        self.assertEqual(encesta.maquina, Maquina.objects.get(id=1))
        self.assertEqual(encesta.cantidad, 1)
        # Borra el contenido de prueba
        encesta.delete()

    # Comprueba que se pueden actualizar contenidos de la cesta
    def test_encesta_update(self):
        # Obtiene un contenido de la cesta de la base de datos
        encesta = EnCesta.objects.get(id=1)
        # Actualiza el contenido
        encesta.cantidad = 2
        encesta.save()
        # Comprueba que el contenido se ha actualizado correctamente
        self.assertEqual(encesta.cantidad, 2)

    # Comprueba que se pueden borrar contenidos de la cesta
    def test_encesta_delete(self):
        # Obtiene un contenido de la cesta de la base de datos
        encesta = EnCesta.objects.get(id=1)
        # Borra el contenido
        encesta.delete()
        # Comprueba que el contenido se ha borrado correctamente
        self.assertRaises(EnCesta.DoesNotExist, EnCesta.objects.get, id=1)

    # Tests de la clase Factura
    # Comprueba que se pueden obtener las facturas de la base de datos
    def test_factura_retrieve(self):
        # Obtiene una factura de la base de datos
        factura = Factura.objects.get(pedido__id=1)
        # Comprueba que la factura se ha obtenido correctamente
        self.assertEqual(factura.pedido, Pedido.objects.get(id=1))
        self.assertEqual(factura.fecha, datetime.date(2021, 1, 1))
        self.assertEqual(factura.nombre_cliente, "Nombre de prueba")
        self.assertEqual(factura.apellidos_cliente, "Apellidos de prueba")
        self.assertEqual(factura.direccion, "Direccion de prueba")
        self.assertEqual(factura.dni, "12345678A")

    # Comprueba que se pueden crear facturas
    def test_factura_create(self):
        # Crea una factura con los datos de prueba
        factura = Factura.objects.create(
            pedido = Pedido.objects.get(id=3),
            fecha = datetime.date(2018, 1, 1),
            nombre_cliente = "Nombre de prueba",
            apellidos_cliente = "Apellidos de prueba",
            direccion = "Direccion de prueba",
            dni = "12345678A"
        )
        # Comprueba que la factura se ha creado correctamente
        self.assertEqual(factura.pedido, Pedido.objects.get(id=3))
        self.assertEqual(factura.fecha, datetime.date(2018, 1, 1))
        self.assertEqual(factura.nombre_cliente, "Nombre de prueba")
        self.assertEqual(factura.apellidos_cliente, "Apellidos de prueba")
        self.assertEqual(factura.direccion, "Direccion de prueba")
        self.assertEqual(factura.dni, "12345678A")
        # Borra la factura de prueba
        factura.delete()

    # Comprueba que se pueden actualizar facturas
    def test_factura_update(self):
        # Obtiene una factura de la base de datos
        factura = Factura.objects.get(pedido__id=1)
        # Actualiza la factura
        factura.dni = "12345678A"
        factura.save()
        # Comprueba que la factura se ha actualizado correctamente
        self.assertEqual(factura.dni, "12345678A")

    # Comprueba que se pueden borrar facturas
    def test_factura_delete(self):
        # Obtiene una factura de la base de datos
        factura = Factura.objects.get(pedido__id=1)
        # Borra la factura
        factura.delete()
        # Comprueba que la factura se ha borrado correctamente
        self.assertRaises(Factura.DoesNotExist, Factura.objects.get, pedido__id=1)

    # Tests de la clase LineaFactura	
    # Comprueba que se pueden obtener las lineas de factura de la base de datos
    def test_lineafactura_retrieve(self):
        # Obtiene una linea de factura de la base de datos
        lineafactura = LineaFactura.objects.get(id=1)
        # Comprueba que la linea se ha obtenido correctamente
        self.assertEqual(lineafactura.factura, Factura.objects.get(pedido__id=1))
        self.assertEqual(lineafactura.nombre, "Nombre de prueba")
        self.assertEqual(lineafactura.iva, 21)
        self.assertEqual(lineafactura.precio_sin_iva, 100)
        self.assertEqual(lineafactura.descuento, 0)
        self.assertEqual(lineafactura.cantidad, 1)

    # Comprueba que se pueden crear lineas de factura
    def test_lineafactura_create(self):
        # Crea una linea de factura con los datos de prueba
        lineafactura = LineaFactura.objects.create(
            factura = Factura.objects.get(pedido__id=1),
            nombre = "Nombre de prueba",
            iva = 21,
            precio_sin_iva = 100,
            descuento = 0,
            cantidad = 1
        )
        # Comprueba que la linea se ha creado correctamente
        self.assertEqual(lineafactura.factura, Factura.objects.get(pedido__id=1))
        self.assertEqual(lineafactura.nombre, "Nombre de prueba")
        self.assertEqual(lineafactura.iva, 21)
        self.assertEqual(lineafactura.precio_sin_iva, 100)
        self.assertEqual(lineafactura.descuento, 0)
        self.assertEqual(lineafactura.cantidad, 1)
        # Borra la linea de prueba
        lineafactura.delete()

    # Comprueba que se pueden actualizar lineas de factura
    def test_lineafactura_update(self):
        # Obtiene una linea de factura de la base de datos
        lineafactura = LineaFactura.objects.get(id=1)
        # Actualiza la linea
        lineafactura.nombre = "Nombre de prueba"
        lineafactura.save()
        # Comprueba que la linea se ha actualizado correctamente
        self.assertEqual(lineafactura.nombre, "Nombre de prueba")

    # Comprueba que se pueden borrar lineas de factura
    def test_lineafactura_delete(self):
        # Obtiene una linea de factura de la base de datos
        lineafactura = LineaFactura.objects.get(id=1)
        # Borra la linea
        lineafactura.delete()
        # Comprueba que la linea se ha borrado correctamente
        self.assertRaises(LineaFactura.DoesNotExist, LineaFactura.objects.get, id=1)