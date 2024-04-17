from django.http import HttpResponseRedirect
from django.db.models import Count

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
    groupes_counts = Groupe.objects.annotate(num_utilisateurs=Count('utilisateurs'))
    counts_dict = (
        groupes_counts
        .values('num_utilisateurs')
        .annotate(num_groupes=Count('id', distinct=True))
    )
    resultats = {item['num_utilisateurs']: item['num_groupes'] for item in counts_dict}

    print(resultats)
    return resultats.get(config.group_size,False)
    