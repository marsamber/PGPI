from django.conf import settings
from django.shortcuts import redirect, render

from app.forms import SearchForm

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
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')



def catalogo(request, categoria):
    search = request.session.get('search')
    productos = []

    if search:
        del request.session['search']
        # productos = Producto.objects.filter(nombre__icontains=search)
    else:
        pass
        # productos = Producto.objects.filter(categoria=categoria)

    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])
    
    return render(request, 'catalogo.html', {'categoria': categoria, 'productos': productos, 'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

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

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'domicilioPago.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def datosPago(request):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'datosPago.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def pago(request):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'pago.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

def confirmacion(request):
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'confirmacion.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

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