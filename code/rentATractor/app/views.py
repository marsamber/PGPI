from django.conf import settings
from django.shortcuts import render

from app.forms import SearchForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def catalogo(request, categoria):
    formulario = SearchForm()
    productos = []

    # if request.method == 'POST':
    #     formulario = SearchForm(request.POST)
    #     if formulario.is_valid():
    #         busqueda = formulario.cleaned_data['search']
    #         productos = Producto.objects.filter(nombre__icontains=busqueda)
    # else:
    #     productos = Producto.objects.filter(categoria=categoria)
    
    return render(request, 'catalogo.html', {'categoria': categoria, 'formulario': formulario, 'productos': productos, 'STATIC_URL':settings.STATIC_URL})

def producto(request, nombre):
    print(nombre)
    return render(request, 'producto.html', {'nombre': nombre, 'STATIC_URL':settings.STATIC_URL})

def cesta(request):
    return render(request, 'cesta.html')

def domicilioPago(request):
    return render(request, 'domicilioPago.html')

def datosPago(request):
    return render(request, 'datosPago.html')

def pago(request):
    return render(request, 'pago.html')

def confirmacion(request):
    return render(request, 'confirmacion.html')

def miCuenta(request):
    return render(request, 'miCuenta.html')

def favoritos(request):
    return render(request, 'favoritos.html')

def misCompras(request):
    return render(request, 'misCompras.html')