"""rentATractor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views
import django.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="homepage"),
    path('login/', views.login),
    path('logout/', views.logout),
    path('autenticar/', views.autenticar),
    path('register/', views.register),
    path('catalogo/<str:categoria>',views.catalogo),
    path('producto/<int:id>',views.producto),
    path('cesta/', views.cesta),
    path('domicilioPago/', views.domicilioPago),
    path('datosPago/', views.datosPago),
    path('pago/', views.payment_checkout),
    path('confirmacion/<int:id>', views.confirmacion),
    path('cancelar/', views.cancelar),
    path('miCuenta/', views.miCuenta),
    path('favoritos/', views.favoritos),
    path('favoritos/<int:id>', views.addFavorito),
    path('misPedidos/', views.misPedidos),
    path('sobreNosotros/', views.sobreNosotros),
    path('contacto/', views.contacto),
    path('atencionCliente/', views.atencionCliente),
    path('seguimientoPedidos/', views.seguimientoPedidos),
    path('politicaDevolucion/', views.politicaDevolucion),
    path('reclamaciones/', views.reclamaciones),
    path('opinion/<int:pedido>', views.opinion),
    path('terminosCondicionesUso/', views.terminosCondicionesUso),
    path('politicaPrivacidad/', views.politicaPrivacidad),
    path('media/<path>', django.views.static.serve,
         {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
