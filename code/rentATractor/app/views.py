from argparse import _get_action_name
from distutils.command import clean
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

from app.forms import OrderForm, SearchForm
from app.models import ClienteRegistrado, Contiene, EnCesta, Maquina, Opinion, Pedido
import stripe
from app.forms import OrderForm, SearchForm, ContactForm, ComplaintForm, Step1Form, OpinionForm
from .models import Maquina, Opinion, Pedido, Reclamacion

# Create your views here.
def index(request):
    cesta = EnCesta.objects.filter(cliente__id = 1)

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])


    return render(request, 'index.html', {'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def login(request):

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'login.html', {'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})


def register(request):

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'register.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def catalogo(request, categoria):
    search = request.session.get('search')
    orden = ""
    productos = []
    favoritos = ClienteRegistrado.objects.get(cliente__id = 1).gusta.all()
    tipoMaquina = categoriaToTipoMaquina(categoria)

    cesta = EnCesta.objects.filter(cliente__id = 1)

    formulario = SearchForm()
    formularioOrdenacion = OrderForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        formularioOrdenacion = OrderForm(request.POST)
        if request.POST.get('search') != None and request.POST.get('search') != "":
            if formulario.is_valid():
                request.session['search'] = formulario.cleaned_data['search']
                return redirect('/catalogo/Resultados de: ' + request.session['search'])
        if formularioOrdenacion.is_valid():
            orden = request.POST.get('order')
            print(orden)
            if orden == 'name asc':
                if search:
                    productos = Maquina.objects.filter(nombre__icontains=search).order_by('nombre')
                else: 
                    productos = Maquina.objects.filter(tipo_maquina__icontains=tipoMaquina).order_by('nombre')
                print(productos)
            elif orden == 'name desc':
                if search:
                    productos = Maquina.objects.filter(nombre__icontains=search).order_by('-nombre')
                else: 
                    productos = Maquina.objects.filter(tipo_maquina__icontains=tipoMaquina).order_by('-nombre')
                print(productos)
            elif orden == 'price asc':
                if search:
                    productos = Maquina.objects.filter(nombre__icontains=search).order_by('precio')
                else: 
                    productos = Maquina.objects.filter(tipo_maquina__icontains=tipoMaquina).order_by('precio')
                print(productos)
            elif orden == 'price desc':
                if search:
                    productos = Maquina.objects.filter(nombre__icontains=search).order_by('-precio')
                else: 
                    productos = Maquina.objects.filter(tipo_maquina__icontains=tipoMaquina).order_by('-precio')
                print(productos)
            elif orden == 'ordenar':
                if search:
                    productos = Maquina.objects.filter(nombre__icontains=search)
                else: 
                    productos = Maquina.objects.filter(tipo_maquina__icontains=tipoMaquina)
    
    if search and not categoria.startswith('Resultados de: ') and orden == "":
        del request.session['search']
        productos = Maquina.objects.filter(tipo_maquina__icontains=tipoMaquina)
    elif not search and orden == "":
        productos = Maquina.objects.filter(tipo_maquina__icontains=tipoMaquina)
    elif search and orden == "":
        productos = Maquina.objects.filter(nombre__icontains=search)
    
    return render(request, 'catalogo.html', {'categoria': categoria, 'productos': productos, 'favoritos': favoritos, 'cesta': cesta, 'formulario': formulario, 'formularioOrdenacion': formularioOrdenacion, 'orden': orden, 'STATIC_URL':settings.STATIC_URL})

def producto(request, id):
    producto = Maquina.objects.get(id=id)
    opiniones = Opinion.objects.filter(maquina__id=id)
    print(opiniones)
    sugerencias = Maquina.objects.filter(tipo_maquina__icontains=producto.tipo_maquina).exclude(id=id).order_by('?')[:3]

    cesta = EnCesta.objects.filter(cliente__id = 1)

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'producto.html', {'producto': producto, 'sugerencias': sugerencias, 'opiniones': opiniones, 'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def cesta(request):
    precioTotal = 0 
    favoritos = ClienteRegistrado.objects.get(cliente__id = 1).gusta.all()
    cesta = EnCesta.objects.filter(cliente__id = 1)

    for producto in cesta:
        precioTotal += (producto.maquina.precio - producto.maquina.descuento) * producto.cantidad

    precioTotalEnvio = precioTotal + 50

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'cesta.html', {'precioTotal': precioTotal, 'precioTotalEnvio': precioTotalEnvio, 'favoritos': favoritos, 'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def domicilioPago(request):
    precioTotal = 0 
    cesta = EnCesta.objects.filter(cliente__id = 1)

    for producto in cesta:
        precioTotal += (producto.maquina.precio - producto.maquina.descuento) * producto.cantidad

    precioTotalEnvio = precioTotal + 50

    formulario = SearchForm()
    form = Step1Form()

    if request.method == 'POST':
        form = Step1Form(request.POST)

        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'domicilioPago.html', {'precioTotal': precioTotal, 'precioTotalEnvio': precioTotalEnvio, 'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def datosPago(request):
    precioTotal = 0
    cesta = EnCesta.objects.filter(cliente__id = 1)

    for producto in cesta:
        precioTotal += (producto.maquina.precio - producto.maquina.descuento) * producto.cantidad

    precioTotalEnvio = precioTotal + 50

    formulario = SearchForm()
    form = Step1Form()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'datosPago.html', {'precioTotal': precioTotal, 'precioTotalEnvio': precioTotalEnvio, 'cesta': cesta, 'formulario': formulario, 'form': form, 'STATIC_URL':settings.STATIC_URL})

def pago(request):
    cesta = EnCesta.objects.filter(cliente__id = 1)

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'pago.html', {'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def payment_checkout(request):
    stripe.api_key = 'sk_test_51M7jbDAogMfbRmsAelkebvd3Wsk0oeabaTqNZ959kYwIwazCJyYjOfE2N90zlDtieXZlxB41iNnEMEei0pnCw9YM000Tl9hu0p'
    session = stripe.checkout.Session.create(
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': 'maquina',
        },
        'unit_amount': 2000,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url='http://localhost:8000/confirmacion/',
    cancel_url='http://localhost:8000/cancelar/',
  )

    return redirect(session.url)

def confirmacion(request, id):
    pedido = Pedido.objects.get(id=id)
    contiene = Contiene.objects.filter(pedido__id=id)
    precioTotal = 0

    for c in contiene:
        precioTotal += (c.maquina.precio - c.maquina.descuento) * c.cantidad
    
    precioTotalEnvio = precioTotal + 50

    cesta = EnCesta.objects.filter(cliente__id = 1)

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'confirmacion.html', {'pedido': pedido, 'contiene': contiene, 'precioTotal': precioTotal, 'precioTotalEnvio': precioTotalEnvio, 'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def cancelar(request):
    cesta = EnCesta.objects.filter(cliente__id = 1)

    return render(request, 'cancelar.html', {'cesta': cesta, 'STATIC_URL':settings.STATIC_URL})

def miCuenta(request):
    cesta = EnCesta.objects.filter(cliente__id = 1)

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'miCuenta.html', {'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def favoritos(request):
    favoritos = ClienteRegistrado.objects.get(cliente__id=1).gusta.all()

    cesta = EnCesta.objects.filter(cliente__id = 1)
    
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'favoritos.html', {'productos': favoritos, 'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def misPedidos(request):
    pedidos = Pedido.objects.filter(cliente__id=1)

    cesta = EnCesta.objects.filter(cliente__id = 1)

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
            
    return render(request, 'misPedidos.html', {'pedidos': pedidos, 'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def sobreNosotros(request):
    cesta = EnCesta.objects.filter(cliente__id = 1)

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'sobreNosotros.html', {'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def contacto(request):
    cesta = EnCesta.objects.filter(cliente__id = 1)

    formulario = SearchForm()
    form = ContactForm()
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'email': form.cleaned_data['email'],
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, body.get(0), ['iredomgar4@alum.us.es'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('/contacto?submitted=True')
        
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
    
    else:
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'contacto.html', {'cesta': cesta, 'formulario': formulario, 'form': form, 'STATIC_URL':settings.STATIC_URL})

def atencionCliente(request):
    cesta = EnCesta.objects.filter(cliente__id = 1)

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'atencionCliente.html', {'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def seguimientoPedidos(request):
    cesta = EnCesta.objects.filter(cliente__id = 1)

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'seguimientoPedidos.html', {'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def politicaDevolucion(request):
    cesta = EnCesta.objects.filter(cliente__id = 1)

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'politicaDevolucion.html', {'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def reclamaciones(request):
    cesta = EnCesta.objects.filter(cliente__id = 1)
    
    form=ComplaintForm()
    formulario = SearchForm()
    submitted = False

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            reclamacion = Reclamacion()
            reclamacion.cuerpo = form.cleaned_data['message']
            idPedido = form.cleaned_data['order']
            reclamacion.pedido = Pedido.objects.get(id=idPedido)
            idMaquina = form.cleaned_data['machine']
            reclamacion.maquina = Maquina.objects.get(id=idMaquina)
            reclamacion.save()
            request.session['name'] = form.cleaned_data['name']
            request.session['email'] = form.cleaned_data['email']
        
            return redirect('/reclamaciones?submitted=True')

        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    else:
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'reclamaciones.html', {'cesta': cesta, 'formulario': formulario, 'form': form, 'STATIC_URL':settings.STATIC_URL, 'submitted': submitted})


def opinion(request, pedido):
    form = OpinionForm()
    formulario = SearchForm()
    submitted = False
 

    if request.method == 'POST':
        form = OpinionForm(request.POST)
        if form.is_valid():
            opinion = Opinion()
            idPedido = pedido
            print(pedido)
            opinion.pedido = Pedido.objects.get(id=idPedido)
            idMaquina = form.cleaned_data['machine']
            if Pedido.objects.filter(maquina=Maquina.objects.get(id=idMaquina)).exists():
                opinion.maquina = Maquina.objects.get(id=idMaquina)
                opinion.cuerpo = form.cleaned_data['message']
                opinion.save()
                return redirect('/opinion/' + str(pedido) + '?submitted=True')
            else:
                form._errors['machine'] = form.add_error('machine', '')
             

        # formulario = SearchForm(request.POST)
        # if formulario.is_valid():
        #     request.session['search'] = formulario.cleaned_data['search']
        #     return redirect('/catalogo/Resultados de: ' + request.session['search'])
        
    else:
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'opinion.html', {'formulario': formulario, 'form': form, 'STATIC_URL': settings.STATIC_URL, 'submitted': submitted})


def terminosCondicionesUso(request):
    cesta = EnCesta.objects.filter(cliente__id = 1)

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'terminosCondicionesUso.html', {'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def politicaPrivacidad(request):
    cesta = EnCesta.objects.filter(cliente__id = 1)

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'politicaPrivacidad.html', {'cesta': cesta, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})
   
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