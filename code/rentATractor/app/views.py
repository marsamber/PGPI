from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def cesta(request):
    return render(request, 'cesta.html')