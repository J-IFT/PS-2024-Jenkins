from django import forms
from django.forms import ModelForm

from gestiongroupes.models import GroupConfig


class ConnectionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur :", max_length=25)


class GroupConfigForm(ModelForm):
    # Obligé de redéfinir le champ pour l'afficher en radio plutôt que select
    LAST_GROUP_CHOICES = [
        ('LAST_MAX', 'Plus grand'),
        ('LAST_MIN', 'Plus petit')
    ]

    last_group = forms.ChoiceField(choices=LAST_GROUP_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = GroupConfig
        fields = ['max_users', 'max_groups', 'last_group']
