from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def cesta(request):
    return render(request, 'cesta.html')

def miCuenta(request):
    return render(request, 'miCuenta.html')

def favoritos(request):
    return render(request, 'favoritos.html')

def misCompras(request):
    return render(request, 'misCompras.html')