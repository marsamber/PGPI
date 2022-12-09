from django import forms

from .models import Maquina, Pedido


class SearchForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control me-2", "placeholder": "Busca productos"}), label=False,
        required=False)


class LoginForm(forms.Form):
    template_name = "login_snippet.html"
    user = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
                           required=True, label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
                               required=True, label='Contraseña')


class OrderForm(forms.Form):
    order = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-select", "onchange": "this.form.submit()"}),
                              choices=[("ordenar", "Ordenar por"), ("name asc", "Nombre ascendente"), (
                                  "name desc", "Nombre descendente"), ("price asc", "Precio ascendente"),
                                       ("price desc", "Precio descendente")], label=False, initial="ordenar",
                              required=False)


class RegisterForm(forms.Form):
    template_name = 'register_snippet.html'
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), label='Nombre')
    apellidos = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), label='Apellidos')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control"}), label='Correo electrónico')
    dni = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), label='DNI')
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'class': "form-control"}),
                                       label='Fecha de nacimiento')
    usuario = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}), label='Contraseña')
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), label='Dirección')


class MiCuentaForm(forms.Form):
    template_name = 'micuenta_snippet.html'
    nombre = forms.CharField(widget=(forms.TextInput(attrs={'class': "form-control"})), label='Nombre')
    apellidos = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), label='Apellidos')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control"}), label='Correo electrónico')
    dni = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), label='DNI')
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'class': "form-control"}),
                                       label='Fecha de nacimiento')
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), label='Dirección',
                                required=False)


class ContactForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "Email"}), label="Correo electrónico", required=True)
    subject = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "Asunto del mensaje"}), label="Asunto", required=True)
    message = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control me-2", "placeholder": "Descripción del mensaje"}), label="Mensaje", required=True)


class ComplaintForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "Nombre del cliente"}), label="Nombre", required=True)
    email = forms.EmailField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "Email"}), label="Correo electrónico", required=True)
    order = forms.IntegerField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "XXXX"}), label="Número de pedido", required=True)
    machine = forms.IntegerField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "XXXX"}), label="Número de máquina", required=True)
    message = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control me-2", "placeholder": "Descripción del problema"}), label="Mensaje",
        required=True)


class OpinionForm(forms.Form):
    machine = forms.IntegerField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "XXXX"}), label="Número de referencia del producto",
        required=True)
    message = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control me-2", "placeholder": "Escribe tu opinión"}), label="Mensaje", required=True)


class Step1Form(forms.Form):
    template_name='domicilioPago_snippet.html'
    name = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control me-2 ", "placeholder": "Nombre"}), label="Nombre", required=True)
    surname = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control me-2 ", "placeholder": "Apellidos"}), label="Apellidos", required=True)
    address = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "Nombre de la Vía"}), label="Dirección", required=True)
    # phone = forms.CharField(widget=forms.TextInput(
    #     attrs={"class": "form-control me-2", "placeholder": "XXXXXXXXX"}), label="Teléfono", required=True)
    dni = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "XXXXXXXXX"}), label="DNI", required=True)
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'class': "form-control me-2", 'placeholder': 'dd/mm/yyyy'}),
        label='Fecha de nacimiento', required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control me-2"}), label='Correo eléctronico')


class SeguimientoPedidoForm(forms.Form):
    idPedido = forms.IntegerField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "Introduzca el número de su pedido"}), label=False,
                                  required=True)
