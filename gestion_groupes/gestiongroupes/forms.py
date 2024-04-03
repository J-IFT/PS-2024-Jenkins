from django import forms


class ConnectionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur :", max_length=25)


class GroupConfigForm(forms.Form):
    LAST_GROUP_CHOICES = [
        ('LAST_MAX', 'Plus grand'),
        ('LAST_MIN', 'Plus petit')
    ]

    max_users = forms.IntegerField(label="Nombre max. d'utilisateurs")
    max_groups = forms.IntegerField(label="Nombre max. de groupes")
    last_group = forms.ChoiceField(label="Configuration du dernier groupe", choices=LAST_GROUP_CHOICES,
                                   widget=forms.RadioSelect())
