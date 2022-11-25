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

from app.forms import OrderForm, SearchForm, ContactForm, ComplaintForm, Step1Form, OpinionForm
from .models import Maquina, Opinion, Pedido, Reclamacion

# Create your views here.
def index(request):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'index.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def login(request):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'login.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})


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
            orden = request.POST.get('orden')
            # if orden == 'name asc':
            #     productos = productos.order_by('nombre')
            # elif orden == 'name desc':
            #     productos = productos.order_by('-nombre')
            # elif orden == 'price asc':
            #     productos = productos.order_by('precio')
            # elif orden == 'price desc':
            #     productos = productos.order_by('-precio')
            # elif orden == 'ordenar':
            #     pass
    
    if search and not categoria.startswith('Resultados de: '):
        del request.session['search']
        # productos = Producto.objects.filter(categoria=categoria)
    elif search:
        pass
        # productos = Producto.objects.filter(nombre__icontains=search)
    
    return render(request, 'catalogo.html', {'categoria': categoria, 'productos': productos, 'formulario': formulario, 'formularioOrdenacion': formularioOrdenacion, 'orden': orden, 'STATIC_URL':settings.STATIC_URL})

def producto(request, nombre):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'producto.html', {'nombre': nombre, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def cesta(request):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'cesta.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def domicilioPago(request):
    formulario = SearchForm()
    form = Step1Form()

    if request.method == 'POST':
        form = Step1Form(request.POST)

        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'domicilioPago.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def datosPago(request):
    formulario = SearchForm()
    form = Step1Form()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'datosPago.html', {'formulario': formulario, 'form': form, 'STATIC_URL':settings.STATIC_URL})

def pago(request):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'pago.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def confirmacion(request, pedido):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'confirmacion.html', {'pedido': pedido, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def miCuenta(request):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'miCuenta.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def favoritos(request):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'favoritos.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def misCompras(request):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
            
    return render(request, 'misCompras.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def sobreNosotros(request):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'sobreNosotros.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def contacto(request):
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

    return render(request, 'contacto.html', {'formulario': formulario, 'form': form, 'STATIC_URL':settings.STATIC_URL, 'submitted': submitted})

def atencionCliente(request):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'atencionCliente.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def seguimientoPedidos(request):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'seguimientoPedidos.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def politicaDevolucion(request):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'politicaDevolucion.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def reclamaciones(request):
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

    return render(request, 'reclamaciones.html', {'formulario': formulario, 'form': form, 'STATIC_URL':settings.STATIC_URL, 'submitted': submitted})


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
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'terminosCondicionesUso.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def politicaPrivacidad(request):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'politicaPrivacidad.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})
   
