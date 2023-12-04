from django import forms
from client.models import Client


class AddClientForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    