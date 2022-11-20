from django.conf import settings
from django.shortcuts import redirect, render

from app.forms import OrderForm, SearchForm

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

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'contacto.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

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
    formulario = SearchForm()

    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            request.session['search'] = formulario.cleaned_data['search']
            return redirect('/catalogo/Resultados de: ' + request.session['search'])

    return render(request, 'reclamaciones.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})

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
   
