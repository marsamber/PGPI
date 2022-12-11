import datetime
from argparse import _get_action_name
from distutils.command import clean
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from pathlib import Path
from pyexpat import model
from pyexpat.errors import messages
import socket
from django import forms
from django.conf import settings
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User
from app.forms import OrderForm, SearchForm, LoginForm
from app.models import ClienteRegistrado, Contiene, EnCesta, Maquina, Opinion, Pedido
import stripe
from app.forms import OrderForm, SearchForm, ContactForm, ComplaintForm, Step1Form, OpinionForm, MiCuentaForm, \
    RegisterForm, SeguimientoPedidoForm, Step2Form
from .models import Maquina, Opinion, Pedido, Reclamacion, Cliente, EstadoPedido
from django.contrib.auth import authenticate, login as log, logout as django_logout
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.template.loader import get_template
from weasyprint import HTML
from django.http import FileResponse
from django.core.validators import validate_email
import os


# Create your views here.
def index(request):
    cesta = []
    favoritos = []
    noCliente = False
    productos = Maquina.objects.all().filter(sugerido=True)

    formulario = SearchForm(initial={'search': None})

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
        favoritos = ClienteRegistrado.objects.get(cliente__id=cliente.id).gusta.all()
    except ObjectDoesNotExist:
        cliente = None
        noCliente = True
        cesta = verCestaModal(request)
    return render(request, 'index.html',
                  {'cesta': cesta, 'productos': productos, 'favoritos': favoritos, 'formulario': formulario,
                   'STATIC_URL': settings.STATIC_URL, 'cliente': cliente, 'noCliente': noCliente})


def login(request):
    cesta = []
    formulario = SearchForm(initial={'search': None})
    login_form = LoginForm()
    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
    except ObjectDoesNotExist:
        cliente = None
    return render(request, 'login.html', {'cesta': cesta, 'formulario': formulario, 'login_form': login_form,
                                          'STATIC_URL': settings.STATIC_URL, 'cliente': cliente})


def logout(request):
    # if request.method == 'POST':
    django_logout(request)
    return redirect('/')


def autenticar(request):
    formulario = SearchForm(initial={'search': None})
    if request.method == 'POST':
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
        user_name = request.POST['user']
        password = request.POST['password']
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            log(request, user)
            return redirect('/')
        else:
            cesta = EnCesta.objects.filter(cliente__id=1)
    return render(request, "login_error.html", {'cesta': cesta, 'formulario': formulario,
                                                'STATIC_URL': settings.STATIC_URL})


def register(request):
    formulario = SearchForm(initial={'search': None})
    register_form = RegisterForm()
    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        register_form = RegisterForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
        if register_form.is_valid() and register_form.has_changed():
            try:
                cliente = Cliente.objects.get(dni=register_form.cleaned_data['dni'])
            except ObjectDoesNotExist:
                cliente = Cliente(nombre=register_form.cleaned_data['nombre'],
                                  apellidos=register_form.cleaned_data['apellidos'],
                                  dni=register_form.cleaned_data['dni'],
                                  fecha_nacimiento=register_form.cleaned_data['fecha_nacimiento'],
                                  correo=register_form.cleaned_data['email'])
                cliente.save()

            user = User.objects.create_user(register_form.cleaned_data['usuario'], register_form.cleaned_data['email'],
                                            register_form.cleaned_data['password'])
            cliente = Cliente.objects.get(dni=cliente.dni)
            cliente_registrado = ClienteRegistrado(user=user, cliente=cliente,
                                                   direccion=register_form.cleaned_data['direccion'])
            cliente_registrado.save()
            return redirect('/')
    return render(request, 'register.html',
                  {'formulario': formulario, 'STATIC_URL': settings.STATIC_URL, 'register_form': register_form})


def catalogo(request, categoria):
    search = request.session.get('search')
    orden = ""
    productos = []
    favoritos = []
    cesta = []
    noCliente = False
    tipoMaquina = categoriaToTipoMaquina(categoria)

    formulario = SearchForm(initial={'search': None})
    formularioOrdenacion = OrderForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        formularioOrdenacion = OrderForm(request.POST)
        if request.POST.get('search') != None and request.POST.get('search') != "":
            if formulario.is_valid() and formulario.has_changed():
                request.session['search'] = formulario.cleaned_data['search']
                return redirect('/catalogo/Resultados de: ' + request.session['search'])
        if formularioOrdenacion.is_valid():
            orden = request.POST.get('order')
            if orden == 'name asc':
                if search:
                    productos = Maquina.objects.filter(nombre__icontains=search).__or__(
                        Maquina.objects.filter(marca__icontains=search)).__or__(
                        Maquina.objects.filter(fabricante__icontains=search)).order_by('nombre')
                else:
                    productos = Maquina.objects.filter(tipo_maquina__icontains=tipoMaquina).order_by('nombre')
            elif orden == 'name desc':
                if search:
                    productos = Maquina.objects.filter(nombre__icontains=search).__or__(
                        Maquina.objects.filter(marca__icontains=search)).__or__(
                        Maquina.objects.filter(fabricante__icontains=search)).order_by('-nombre')
                else:
                    productos = Maquina.objects.filter(tipo_maquina__icontains=tipoMaquina).order_by('-nombre')
                print(productos)
            elif orden == 'price asc':
                if search:
                    productos = Maquina.objects.filter(nombre__icontains=search).__or__(
                        Maquina.objects.filter(marca__icontains=search)).__or__(
                        Maquina.objects.filter(fabricante__icontains=search)).order_by('precio')
                else:
                    productos = Maquina.objects.filter(tipo_maquina__icontains=tipoMaquina).order_by('precio')
                print(productos)
            elif orden == 'price desc':
                if search:
                    productos = Maquina.objects.filter(nombre__icontains=search).__or__(
                        Maquina.objects.filter(marca__icontains=search)).__or__(
                        Maquina.objects.filter(fabricante__icontains=search)).order_by('-precio')
                else:
                    productos = Maquina.objects.filter(tipo_maquina__icontains=tipoMaquina).order_by('-precio')
                print(productos)
            elif orden == 'ordenar':
                if search:
                    productos = Maquina.objects.filter(nombre__icontains=search).__or__(
                        Maquina.objects.filter(marca__icontains=search)).__or__(
                        Maquina.objects.filter(fabricante__icontains=search))
                else:
                    productos = Maquina.objects.filter(tipo_maquina__icontains=tipoMaquina)

    if search and not categoria.startswith('Resultados de: ') and orden == "":
        del request.session['search']
        productos = Maquina.objects.filter(tipo_maquina__icontains=tipoMaquina)
    elif not search and orden == "":
        productos = Maquina.objects.filter(tipo_maquina__icontains=tipoMaquina)
    elif search and orden == "":
        productos = Maquina.objects.filter(nombre__icontains=search).__or__(
            Maquina.objects.filter(marca__icontains=search)).__or__(
            Maquina.objects.filter(fabricante__icontains=search))
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        favoritos = ClienteRegistrado.objects.get(cliente__id=cliente.id).gusta.all()
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
        noCliente = True
    return render(request, 'catalogo.html',
                  {'categoria': categoria, 'productos': productos, 'favoritos': favoritos, 'cesta': cesta,
                   'formulario': formulario, 'formularioOrdenacion': formularioOrdenacion, 'orden': orden,
                   'STATIC_URL': settings.STATIC_URL, 'cliente': cliente, 'noCliente': noCliente})


def producto(request, id):
    producto = Maquina.objects.get(id=id)
    opiniones = Opinion.objects.filter(maquina__id=id)
    sugerencias = Maquina.objects.filter(tipo_maquina__icontains=producto.tipo_maquina).exclude(id=id).order_by('?')[:3]

    cesta = []

    formulario = SearchForm(initial={'search': None})

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    return render(request, 'producto.html',
                  {'producto': producto, 'sugerencias': sugerencias, 'opiniones': opiniones, 'cesta': cesta,
                   'formulario': formulario, 'STATIC_URL': settings.STATIC_URL, 'cliente': cliente})


def verCestaModal(request):
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
    except ObjectDoesNotExist:
        try:
            device = request.COOKIES['device']
            cliente = Cliente.objects.get(nombre=device)
            favoritos = None
            cesta = EnCesta.objects.filter(cliente__nombre=device)
        except:
            cesta = None
    return cesta


def cesta(request):
    precioTotal = 0
    precioTotalEnvio = 0
    favoritos = []
    cesta = []
    noCliente = False

    formulario = SearchForm(initial={'search': None})

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        favoritos = ClienteRegistrado.objects.get(cliente__id=cliente.id).gusta.all()
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)

        for producto in cesta:
            precioTotal += (producto.maquina.precio - producto.maquina.descuento) * producto.cantidad

        precioTotalEnvio = precioTotal + 50 if precioTotal < 499 else precioTotal
    except ObjectDoesNotExist:
        device = request.COOKIES['device']
        noCliente = True
        try:
            cliente = Cliente.objects.get(nombre=device)
            favoritos = None
            cesta = EnCesta.objects.filter(cliente__nombre=device)

            for producto in cesta:
                precioTotal += (producto.maquina.precio - producto.maquina.descuento) * producto.cantidad

            precioTotalEnvio = precioTotal + 50 if precioTotal < 499 else precioTotal
        except ObjectDoesNotExist:
            cliente = None
            favoritos = None
            cesta = None
    return render(request, 'cesta.html',
                  {'precioTotal': precioTotal, 'precioTotalEnvio': precioTotalEnvio, 'favoritos': favoritos,
                   'cesta': cesta, 'formulario': formulario, 'STATIC_URL': settings.STATIC_URL, 'cliente': cliente,
                   'noCliente': noCliente})


def addCesta(request, id):
    try:
        producto = Maquina.objects.get(pk=id)
        try:
            cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        except ObjectDoesNotExist:
            device = request.COOKIES['device']
            try:
                cliente = Cliente.objects.get(nombre=device)
            except ObjectDoesNotExist:
                clienteDevice = Cliente(nombre=device)
                clienteDevice.save()
                cliente = Cliente.objects.get(nombre=device)

        if EnCesta.objects.filter(cliente=cliente, maquina=producto).exists():
            enCesta = EnCesta.objects.get(cliente=cliente, maquina=producto)
            enCesta.cantidad = enCesta.cantidad + 1
            enCesta.save()
        else:
            EnCesta.objects.create(cliente=cliente, maquina=producto, cantidad=1)

    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def removeCesta(request, id):
    try:
        producto = Maquina.objects.get(pk=id)
        try:
            cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        except ObjectDoesNotExist:
            device = request.COOKIES['device']
            cliente = Cliente.objects.get(nombre=device)
        if EnCesta.objects.filter(cliente=cliente, maquina=producto).exists():
            enCesta = EnCesta.objects.get(cliente=cliente, maquina=producto)
            enCesta.cantidad = 0
            enCesta.delete()
        else:
            pass

    except Exception as e:
        raise e
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def updateCesta(request, id, cantidad):
    try:
        producto = Maquina.objects.get(pk=id)
        try:
            cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        except ObjectDoesNotExist:
            device = request.COOKIES['device']
            cliente = Cliente.objects.get(nombre=device)
        if EnCesta.objects.filter(cliente=cliente, maquina=producto).exists():
            enCesta = EnCesta.objects.get(cliente=cliente, maquina=producto)
            if cantidad == '0':
                enCesta.delete()
            else:
                enCesta.cantidad = cantidad
                enCesta.save()
        else:
            pass

    except Exception as e:
        raise e
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def domicilioPago(request):
    precioTotal = 0
    cesta = []

    try:
        clienteRegistrado = ClienteRegistrado.objects.get(user=request.user.id)
        cliente = clienteRegistrado.cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
        for producto in cesta:
            precioTotal += (producto.maquina.precio - producto.maquina.descuento) * producto.cantidad
            step1_form = Step1Form(
                initial={'name': cliente.nombre, 'surname': cliente.apellidos, 'dni': cliente.dni,
                         'email': cliente.correo,
                         'fecha_nacimiento': cliente.fecha_nacimiento, 'address': clienteRegistrado.direccion})
    except ObjectDoesNotExist:
        device = request.COOKIES['device']
        cliente = Cliente.objects.get(nombre=device)
        noCliente = True
        cesta = verCestaModal(request)
        step1_form = Step1Form()
    formulario = SearchForm(initial={'search': None})

    if request.method == 'POST':

        formulario = SearchForm(request.POST)
        step1_form = Step1Form(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
        if step1_form.is_valid() and step1_form.has_changed():
            cliente.nombre = step1_form.cleaned_data['name']
            cliente.apellidos = step1_form.cleaned_data['surname']
            cliente.dni = step1_form.cleaned_data['dni']
            cliente.email = step1_form.cleaned_data['email']
            if not cliente.id:
                cliente_id = Cliente.objects.count() +1
                try:
                    while(True):
                        cliente_aux = Cliente.objects.get(pk=cliente_id)
                        cliente_id += 1
                except:
                    cliente.id = cliente_id
            cliente.save()
            pedido_id = Pedido.objects.count() + 1
            try:
                while(True):
                    pedido_aux = Pedido.objects.get(pk=pedido_id)
                    pedido_id += 1
            except:
                pedido = Pedido(id=pedido_id, fecha_pedido=datetime.date.today(), cliente=cliente,
                                recogida_en_tienda=step1_form.cleaned_data['tienda'])
            pedido.save()
            cesta = EnCesta.objects.filter(cliente__id=cliente.id)
            for producto in cesta:
                pedido.maquina.add(producto.maquina)
                Contiene(pedido=pedido, maquina=producto.maquina, cantidad=producto.cantidad).save()
        return redirect(f'/pago/{pedido.id}')

    return render(request, 'domicilioPago.html', {'precioTotal': precioTotal, 'cesta': cesta, 'formulario': formulario,
                                                  'STATIC_URL': settings.STATIC_URL, 'cliente': cliente,
                                                  'step1_form': step1_form,'noCliente':noCliente})


def remove_pedido(request, id):
    try:
        Pedido.objects.get(pk=id).delete()
    except:
        pass
    return redirect('/domicilioPago')


def datosPago(request):
    precioTotal = 0
    precioTotalEnvio = 0
    cesta = []
    pedido = Pedido()

    formulario = SearchForm(initial={'search': None})
    step1_form = Step1Form()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=1)

        for producto in cesta:
            precioTotal += (producto.maquina.precio - producto.maquina.descuento) * producto.cantidad

        precioTotalEnvio = precioTotal + 50 if (precioTotal < 499 and not pedido.recogida_en_tienda) else precioTotal

        pedido = Pedido.objects.filter(cliente__id=1).last()
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)

        for producto in cesta:
            precioTotal += (producto.maquina.precio - producto.maquina.descuento) * producto.cantidad

        precioTotalEnvio = precioTotal + 50 if (precioTotal < 499 and not pedido.recogida_en_tienda) else precioTotal

    return render(request, 'datosPago.html',
                  {'precioTotal': precioTotal, 'precioTotalEnvio': precioTotalEnvio, 'pedido': pedido, 'cesta': cesta,
                   'formulario': formulario, 'step1_form': step1_form, 'STATIC_URL': settings.STATIC_URL,
                   'cliente': cliente})


def pago(request, id):
    step2_form = Step2Form()
    formulario = SearchForm(initial={'search': None})
    pedido = Pedido.objects.get(pk=id)
    try:
        cesta = EnCesta.objects.filter(cliente__id=Pedido.objects.get(pk=id).cliente.id)
    except:
        cesta = verCestaModal(request)
    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
        step2_form = Step2Form(request.POST)
        if step2_form.is_valid():
            reembolso = step2_form.cleaned_data['reembolso']
            match reembolso:
                case '1':
                    pedido.estado_pedido = EstadoPedido.comprado
                    pedido.save()
                    for encesta in cesta:
                        encesta.delete()
                    return redirect(f'/confirmacion/{pedido.id}')
                case '2':
                    return payment_checkout(request, id)

    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
    except ObjectDoesNotExist:
        cliente = None
    return render(request, 'pago.html',
                  {'cesta': cesta, 'formulario': formulario, 'STATIC_URL': settings.STATIC_URL, 'cliente': cliente,
                   'pedido': pedido, 'step2_form': step2_form})


def payment_checkout(request, id,):
    stripe.api_key = 'sk_test_51M7jbDAogMfbRmsAelkebvd3Wsk0oeabaTqNZ959kYwIwazCJyYjOfE2N90zlDtieXZlxB41iNnEMEei0pnCw9YM000Tl9hu0p'
    contiene = Contiene.objects.filter(pedido__id=id)

    line_data = []
    for producto in contiene:
        line_data.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': producto.maquina.nombre,
                },
                'unit_amount': int(100*(producto.maquina.precio * (1 - producto.maquina.descuento))),
            },
            'quantity': producto.cantidad,
        })
    session = stripe.checkout.Session.create(
        line_items=line_data, mode='payment',
        success_url=f'http://localhost:8000/confirmacion/{id}',
        cancel_url='http://localhost:8000/cancelar/',
    )

    return redirect(session.url)


def confirmacion(request, id):
    pedido = Pedido.objects.get(id=id)
    contiene = Contiene.objects.filter(pedido__id=id)
    precioTotal = 0
    gastoEnvio = 50

    precioSubtotalEnvio = 0

    for c in contiene:
        precioTotal += (c.maquina.precio - c.maquina.descuento) * c.cantidad

    if precioTotal > 499:
        gastoEnvio = 0

    precioTotalEnvio = precioTotal + gastoEnvio
    iva = precioTotalEnvio * 0.21
    precioSubtotalEnvio = precioTotalEnvio - iva

    cesta = []

    enviado = False

    formulario = SearchForm(initial={'search': None})

    if request.method == 'POST':
        if 'enviar_correo' in request.POST:
            subject = "Confirmación Rent a tractor"
            user = pedido.cliente.correo

            html_message = render_to_string('confirmacionCorreo.html',
                                            {'pedido': pedido, 'Content-ID': '<../../media/logo.png>'})
            plain_message = strip_tags(html_message)

            image_path = './media/logo.png'
            image_name = Path(image_path).name

            email = EmailMultiAlternatives(subject=subject, body=plain_message, from_email=user,
                                           to=['rentatractorus@gmail.com'])
            with open(image_path, mode='rb') as f:
                image = MIMEImage(f.read())
                email.attach(image)
                image.add_header('Content-ID', f"<{image_name}>")
            email.send()
            enviado = True

        if 'descargar_factura' in request.POST:
            template = get_template("factura.html")
            context = {
                "pedido": pedido,
                "icon": '{}{}'.format(settings.MEDIA_URL_F, 'logo.png'),
                "contiene": contiene,
                "precioTotal": precioTotal,
                "precioTotalEnvio": precioTotalEnvio,
                "precioSubtotalEnvio": precioSubtotalEnvio,
                "iva": iva,
                "gastoEnvio": gastoEnvio,
            }
            html_template = template.render(context)

            HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(
                target="app/factura/factura" + str(pedido.id) + ".pdf")
            filepath = os.path.join(settings.BASE_DIR, 'app/factura/factura' + str(pedido.id) + '.pdf')
            print(filepath)
            return FileResponse(open(filepath, 'rb'), content_type='application/pdf')

        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
    else:
        enviado = False

    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)

    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return render(request, 'confirmacion.html', {'pedido': pedido, 'contiene': contiene, 'precioTotal': precioTotal,
                                                 'precioTotalEnvio': precioTotalEnvio,
                                                 'precioSubtotalEnvio': precioSubtotalEnvio,
                                                 'iva': iva, 'gastoEnvio': gastoEnvio, 'cesta': cesta,
                                                 'formulario': formulario, 'STATIC_URL': settings.STATIC_URL,
                                                 'cliente': cliente, 'enviado': enviado})


def factura(request, id):
    pedido = Pedido.objects.get(id=id)
    contiene = Contiene.objects.filter(pedido__id=id)
    precioTotal = 0
    gastoEnvio = 50

    precioSubtotalEnvio = 0

    for c in contiene:
        precioTotal += (c.maquina.precio - c.maquina.descuento) * c.cantidad

    if precioTotal > 499:
        gastoEnvio = 0

    precioTotalEnvio = precioTotal + gastoEnvio
    iva = precioTotalEnvio * 0.21
    precioSubtotalEnvio = precioTotalEnvio - iva

    cesta = []

    enviado = False

    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)

    except ObjectDoesNotExist:
        cliente = None
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return render(request, 'factura.html', {'pedido': pedido, 'contiene': contiene, 'precioTotal': precioTotal,
                                            'precioTotalEnvio': precioTotalEnvio,
                                            'precioSubtotalEnvio': precioSubtotalEnvio, 'iva': iva,
                                            'gastoEnvio': gastoEnvio, 'cesta': cesta, 'STATIC_URL': settings.STATIC_URL,
                                            'cliente': cliente, 'enviado': enviado})


def cancelar(request):
    cesta = []
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    return render(request, 'cancelar.html', {'cesta': cesta, 'STATIC_URL': settings.STATIC_URL, 'cliente': cliente})


def miCuenta(request):
    try:
        clienteRegistrado = ClienteRegistrado.objects.get(user=request.user.id)
        cliente = clienteRegistrado.cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)

        formulario = SearchForm(initial={'search': None})
        micuenta = MiCuentaForm(
            initial={'nombre': cliente.nombre, 'apellidos': cliente.apellidos, 'dni': cliente.dni,
                     'email': cliente.correo,
                     'fecha_nacimiento': cliente.fecha_nacimiento, 'direccion': clienteRegistrado.direccion})

        if request.method == 'POST':
            formulario = SearchForm(request.POST)
            if formulario.is_valid() and formulario.has_changed():
                request.session['search'] = formulario.cleaned_data['search']
                return redirect('/catalogo/Resultados de: ' + request.session['search'])
            micuenta = MiCuentaForm(request.POST)
            if micuenta.is_valid() and micuenta.has_changed():
                cliente.nombre = micuenta.cleaned_data['nombre']
                cliente.apellidos = micuenta.cleaned_data['apellidos']
                cliente.dni = micuenta.cleaned_data['dni']
                cliente.correo = micuenta.cleaned_data['email']
                cliente.fecha_nacimiento = micuenta.cleaned_data['fecha_nacimiento']
                clienteRegistrado.direccion = micuenta.cleaned_data['direccion']
                cliente.save()
                clienteRegistrado.save()

        return render(request, 'miCuenta.html',
                      {'cesta': cesta, 'formulario': formulario, 'STATIC_URL': settings.STATIC_URL, 'cliente': cliente,
                       'micuenta_form': micuenta})
    except ObjectDoesNotExist:
        return redirect('/login')


def favoritos(request):
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        favoritos = ClienteRegistrado.objects.get(cliente=cliente.id).gusta.all()
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)

        formulario = SearchForm(initial={'search': None})

        if request.method == 'POST':
            formulario = SearchForm(request.POST)
            if formulario.is_valid() and formulario.has_changed():
                request.session['search'] = formulario.cleaned_data['search']
                return redirect('/catalogo/Resultados de: ' + request.session['search'])
        return render(request, 'favoritos.html',
                      {'productos': favoritos, 'cesta': cesta, 'formulario': formulario,
                       'STATIC_URL': settings.STATIC_URL,
                       'cliente': cliente})
    except ObjectDoesNotExist:
        return redirect('/login')


def addFavorito(request, id):
    try:
        clienteRegistrado = ClienteRegistrado.objects.get(user=request.user.id)
        producto = Maquina.objects.get(id=id)
        if producto in clienteRegistrado.gusta.all():
            clienteRegistrado.gusta.remove(producto)
            clienteRegistrado.save()
        else:
            clienteRegistrado.gusta.add(producto)
            clienteRegistrado.save()
    except ObjectDoesNotExist:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def misPedidos(request):
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente

        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
        pedidos = Pedido.objects.filter(cliente__id=cliente.id)

        formulario = SearchForm(initial={'search': None})

        if request.method == 'POST':
            formulario = SearchForm(request.POST)
            if formulario.is_valid() and formulario.has_changed():
                request.session['search'] = formulario.cleaned_data['search']
                return redirect('/catalogo/Resultados de: ' + request.session['search'])
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente

        return render(request, 'misPedidos.html',
                      {'pedidos': pedidos, 'cesta': cesta, 'formulario': formulario, 'STATIC_URL': settings.STATIC_URL,
                       'cliente': cliente})
    except ObjectDoesNotExist:
        cliente = None
        return redirect('/login')


def sobreNosotros(request):
    cesta = []

    formulario = SearchForm(initial={'search': None})

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    return render(request, 'sobreNosotros.html',
                  {'cesta': cesta, 'formulario': formulario, 'STATIC_URL': settings.STATIC_URL, 'cliente': cliente})


def contacto(request):
    cesta = []

    formulario = SearchForm(initial={'search': None})
    form = ContactForm()
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Formulario Rent a tractor"
            user = form.cleaned_data['email']
            body = {
                'email': form.cleaned_data['email'],
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'example@mail.com', ['rentatractorus@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('/contacto?submitted=True')

        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    else:
        if 'submitted' in request.GET:
            submitted = True
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    return render(request, 'contacto.html',
                  {'cesta': cesta, 'formulario': formulario, 'form': form, 'STATIC_URL': settings.STATIC_URL,
                   'cliente': cliente, 'submitted': submitted})


def atencionCliente(request):
    cesta = []

    formulario = SearchForm(initial={'search': None})

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    return render(request, 'atencionCliente.html',
                  {'cesta': cesta, 'formulario': formulario, 'STATIC_URL': settings.STATIC_URL, 'cliente': cliente})


def seguimientoPedidos(request):
    cesta = []

    formulario = SearchForm(initial={'search': None})

    form = SeguimientoPedidoForm(initial={'idPedido': None})

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        form = SeguimientoPedidoForm(request.POST)

        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

        if form.is_valid() and form.has_changed():
            idPedido = form.cleaned_data['idPedido']
            if Pedido.objects.filter(id=idPedido).exists():
                return redirect('/confirmacion/' + str(idPedido))
            else:
                form._errors['idPedido'] = form.add_error('idPedido', '')
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    return render(request, 'seguimientoPedidos.html',
                  {'cesta': cesta, 'formulario': formulario, 'form': form, 'STATIC_URL': settings.STATIC_URL,
                   'cliente': cliente})


def politicaDevolucion(request):
    cesta = []

    formulario = SearchForm(initial={'search': None})

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    return render(request, 'politicaDevolucion.html',
                  {'cesta': cesta, 'formulario': formulario, 'STATIC_URL': settings.STATIC_URL, 'cliente': cliente})


def reclamacion(request, pedido):
    cesta = []
    form = ComplaintForm()
    formulario = SearchForm(initial={'search': None})
    submitted = False

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        formulario = SearchForm(initial={'search': None})
        submitted = False

        if form.is_valid():
            reclamacion = Reclamacion()
            idPedido = pedido
            print(pedido)
            reclamacion.pedido = Pedido.objects.get(id=idPedido)
            idMaquina = form.cleaned_data['machine']
            if not Reclamacion.objects.filter(pedido=Pedido.objects.get(id=idPedido),
                                              maquina=Maquina.objects.get(id=idMaquina)).exists():
                if Pedido.objects.filter(maquina=Maquina.objects.get(id=idMaquina)).exists():
                    reclamacion.maquina = Maquina.objects.get(id=idMaquina)
                    reclamacion.cuerpo = form.cleaned_data['message']
                    reclamacion.save()
                    return redirect('/reclamacion/' + str(pedido) + '?submitted=True')
                else:
                    form._errors['machine'] = form.add_error('machine', '')
            else:
                form._errors['machine'] = form.add_error('machine', '')

        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    else:
        if 'submitted' in request.GET:
            submitted = True
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    return render(request, 'reclamacion.html',
                  {'cesta': cesta, 'formulario': formulario, 'form': form, 'STATIC_URL': settings.STATIC_URL,
                   'submitted': submitted, 'cliente': cliente})


def opinion(request, pedido):
    form = OpinionForm()
    formulario = SearchForm(initial={'search': None})
    submitted = False

    if request.method == 'POST':
        form = OpinionForm(request.POST)
        if form.is_valid():
            opinion = Opinion()
            idPedido = pedido
            print(pedido)
            opinion.pedido = Pedido.objects.get(id=idPedido)
            idMaquina = form.cleaned_data['machine']
            if not Opinion.objects.filter(pedido=Pedido.objects.get(id=idPedido),
                                          maquina=Maquina.objects.get(id=idMaquina)).exists():
                if Pedido.objects.filter(maquina=Maquina.objects.get(id=idMaquina)).exists():
                    opinion.maquina = Maquina.objects.get(id=idMaquina)
                    opinion.cuerpo = form.cleaned_data['message']
                    opinion.save()
                    return redirect('/opinion/' + str(pedido) + '?submitted=True')
                else:
                    form._errors['machine'] = form.add_error('machine', '')
            else:
                form._errors['machine'] = form.add_error('machine', '')

        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    else:
        if 'submitted' in request.GET:
            submitted = True
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    return render(request, 'opinion.html',
                  {'formulario': formulario, 'form': form, 'STATIC_URL': settings.STATIC_URL, 'submitted': submitted,
                   'cliente': cliente})


def terminosCondicionesUso(request):
    cesta = []

    formulario = SearchForm(initial={'search': None})

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    return render(request, 'terminosCondicionesUso.html',
                  {'cesta': cesta, 'formulario': formulario, 'STATIC_URL': settings.STATIC_URL, 'cliente': cliente})


def politicaPrivacidad(request):
    cesta = []

    formulario = SearchForm(initial={'search': None})

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    return render(request, 'politicaPrivacidad.html',
                  {'cesta': cesta, 'formulario': formulario, 'STATIC_URL': settings.STATIC_URL, 'cliente': cliente})


def condicionesAlquiler(request):
    cesta = []

    formulario = SearchForm(initial={'search': None})

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
    except ObjectDoesNotExist:
        cliente = None
    return render(request, 'condicionesAlquiler.html',
                  {'cesta': cesta, 'formulario': formulario, 'STATIC_URL': settings.STATIC_URL, 'cliente': cliente})


def politicaEnvio(request):
    cesta = []
    formulario = SearchForm(initial={'search': None})

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
        cesta = EnCesta.objects.filter(cliente__id=cliente.id)
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    return render(request, 'politicaEnvio.html',
                  {'cesta': cesta, 'formulario': formulario, 'STATIC_URL': settings.STATIC_URL, 'cliente': cliente})


def error403(request):
    formulario = SearchForm(initial={'search': None})

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    return render(request, '403_csrf.html',
                  {'STATIC_URL': settings.STATIC_URL, 'formulario': formulario, 'cliente': cliente})


def error404(request):
    formulario = SearchForm(initial={'search': None})

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    return render(request, '404.html',
                  {'STATIC_URL': settings.STATIC_URL, 'formulario': formulario, 'cliente': cliente})


def error500(request):
    formulario = SearchForm(initial={'search': None})

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid() and formulario.has_changed():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    try:
        cliente = ClienteRegistrado.objects.get(user=request.user.id).cliente
    except ObjectDoesNotExist:
        cliente = None
        cesta = verCestaModal(request)
    return render(request, '500.html',
                  {'STATIC_URL': settings.STATIC_URL, 'formulario': formulario, 'cliente': cliente})


def categoriaToTipoMaquina(categoria):
    match categoria:
        case 'Manipulación de cargas':
            return 'manipulacion'
        case 'Movimiento de tierras':
            return 'movimiento'
        case 'Excavadoras':
            return 'excavadoras'
        case 'Plataformas elevadoras':
            return 'plataformas'
        case 'Andamios de aluminio':
            return 'andamios'
        case 'Grúas':
            return 'gruas'
        case 'Maquinaria de hormigón':
            return 'hormigon'
        case 'Herramientas de mano':
            return 'mano'
        case 'Apisonadoras':
            return 'apisonadoras'
        case 'Varios':
            return 'varios'
        case _:
            return 'error'
