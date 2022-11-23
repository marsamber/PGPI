from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control me-2", "placeholder": "Nombre del producto, categoría, fabricante, ..."}), label=False, required=False)


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
