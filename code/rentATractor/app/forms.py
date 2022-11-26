from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control me-2", "placeholder": "Nombre del producto"}), label=False, required=False)

class OrderForm(forms.Form):
    order = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-select", "onchange":"this.form.submit()"}), choices=[("ordenar", "Ordenar por"), ("name asc", "Nombre ascendente"), ("name desc", "Nombre descendente"), ("price asc", "Precio ascendente"), ("price desc", "Precio descendente")], label=False, initial="ordenar", required=False)