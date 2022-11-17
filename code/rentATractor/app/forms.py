from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(label='Buscar', widget=forms.TextInput, required=True)