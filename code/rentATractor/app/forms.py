from django import forms

from .models import Maquina, Pedido


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control me-2", "placeholder": "Nombre del producto"}), label=False, required=False)

class LoginForm(forms.Form):
    template_name = "login_snippet.html"
    user = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Usuario'}),required=True, label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'}),required=True, label='Contraseña')

class OrderForm(forms.Form):
    order = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-select", "onchange": "this.form.submit()"}), choices=[("ordenar", "Ordenar por"), ("name asc", "Nombre ascendente"), (
        "name desc", "Nombre descendente"), ("price asc", "Precio ascendente"), ("price desc", "Precio descendente")], label=False, initial="ordenar", required=False)


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
        attrs={"class": "form-control me-2", "placeholder": "Descripción del problema"}), label="Mensaje", required=True)

class OpinionForm(forms.Form):
    machine = forms.IntegerField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "XXXX"}), label="Número de máquina", required=True)
    message = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control me-2", "placeholder": "Escribe tu opinión"}), label="Mensaje", required=True)

    

class Step1Form(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control me-2 ", "placeholder": "Nombre"}), label="Nombre", required=True)
    surname = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control me-2 ", "placeholder": "Apellidos"}), label="Apellidos", required=True)
    address = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "Nombre de la Vía"}), label="Dirección", required=True)
    number = forms.IntegerField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "XXX"}), label="Número", required=True)
    cp = forms.IntegerField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "XXXXX"}), label="Código Postal", required=True)
    city = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "Nombre de la población"}), label="Población", required=True)
    province = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "Nombre de la provincia"}), label="Provincia", required=True)
    country = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "Nombre del país"}), label="País", required=True)
    phone = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control me-2", "placeholder": "XXXXXXXXX"}), label="País", required=True)
