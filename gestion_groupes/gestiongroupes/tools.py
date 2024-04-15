from django.http import HttpResponseRedirect

from .models import GroupConfig, Groupe, Utilisateur

def init(request):
    # Vérification de l'user
    if 'username' in request.session:
        username = request.session['username']
        try:
            current_user = Utilisateur.objects.get(nom=username)
        except Utilisateur.DoesNotExist:
            del request.session['username']
            return False
    else:
        return False
    # Déconnexion
    if 'disconnect' in request.GET and request.GET['disconnect'] == '1':
        current_user.delete()
        del request.session['username']
        return False
    
    return current_user