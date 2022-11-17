from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

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