from django import forms


class ConnectionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur :", max_length=25)
