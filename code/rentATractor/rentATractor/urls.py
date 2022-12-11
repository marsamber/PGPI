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
    path('login', views.login),
    path('logout/', views.logout),
    path('register/', views.register),
    path('catalogo/<str:categoria>',views.catalogo),
    path('producto/<int:id>',views.producto),
    path('cesta/', views.cesta),
    path('cesta/<int:id>/', views.addCesta),
    path('cesta/remove/<int:id>/', views.removeCesta),
    path('cesta/update/<int:id>/<int:cantidad>/', views.updateCesta),
    path('domicilioPago/', views.domicilioPago),
    path('borraPedido/<int:id>', views.remove_pedido),
    path('create-checkout-session', views.payment_checkout),
    path('pago/<int:id>', views.pago),
    path('confirmacion/<int:id>', views.confirmacion),
    path('factura/<int:id>', views.factura),
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
    path('politicaEnvio/', views.politicaEnvio),
    path('reclamacion/<int:pedido>', views.reclamacion),
    path('opinion/<int:pedido>', views.opinion),
    path('terminosCondicionesUso/', views.terminosCondicionesUso),
    path('politicaPrivacidad/', views.politicaPrivacidad),
    path('condicionesAlquiler/', views.condicionesAlquiler),
    path('media/<path>', django.views.static.serve,
         {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
