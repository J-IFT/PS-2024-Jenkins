from django.http import HttpResponseRedirect
from django.db.models import Count
from collections import defaultdict
from .models import GroupConfig, Groupe, Utilisateur

def init(request):
    # Vérification de l'user
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            current_user = Utilisateur.objects.get(id=user_id)
        except Utilisateur.DoesNotExist:
            del request.session['user_id']
            return False
    else:
        return False
    # Déconnexion
    if 'disconnect' in request.GET and request.GET['disconnect'] == '1':
        current_user.delete()
        del request.session['user_id']
        return False

    return current_user

def get_group_config():
    # On récupére la config des groupes
    try:
        config = GroupConfig.objects.get(pk=1)
    except GroupConfig.DoesNotExist:
        config = GroupConfig()
    return config

def get_nb_group_with_max_members():
    config = get_group_config()
    groupes = Groupe.objects.all()

    groupes_utilisateurs = defaultdict(int)

	# On remplis le dictionnaire avec le nombre de groupe par nombre de membres de ces groupes
    for groupe in groupes:
        nombre_utilisateurs = groupe.utilisateurs.count()
        groupes_utilisateurs[nombre_utilisateurs] += 1

    # On retourne le nombre de groupe ayant le nombre max de membres
    if config.group_size in groupes_utilisateurs:
        return groupes_utilisateurs[config.group_size]
    else:
        return False
