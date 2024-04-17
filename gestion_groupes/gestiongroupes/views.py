from math import floor, ceil
from random import random

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Count

from .forms import ConnectionForm, GroupConfigForm
from .models import GroupConfig, Groupe, Utilisateur

from .tools import init, get_group_config, get_nb_group_with_max_members

def get_group_sizes(max_users, max_groups, last_group):
    base_size = max_users // max_groups
    remainder = max_users % max_groups

    last_group_size = base_size + remainder

    # Le résultat correspond à la demande MAIS pas à l'exemple donné par le prof :
    # Si la configuration vaut LAST_MAX, le dernier groupe a plus d’utilisateurs que les autres
    # (ex : 19 utilisateurs et 5 groupes => 5 groupes de 3 et 1 groupe de 4)
    # 5 + 1 = 6, aka plus que le nombre demandé par l'utilisateur
    if remainder != 0 and last_group == 'LAST_MIN':
        return base_size + 1, last_group_size - (max_groups - 1)

    return base_size, last_group_size


def index(request):
    # session.get('username') plutôt que session['username'] pour éviter erreur si ['username'] n'existe pas encore

    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            # Création User
            username = form.cleaned_data['username']
            utilisateur = Utilisateur.objects.create(nom=username)
            request.session['user_id'] = utilisateur.id            
            utilisateur.save()
            if username == 'admin':
                return HttpResponseRedirect('/config/')
            return HttpResponseRedirect('/liste/')
    
    current_user = init(request)
    if current_user != False:
        if current_user.nom == 'admin':
            return HttpResponseRedirect('/config/')

        return HttpResponseRedirect('/liste/')

    form = ConnectionForm()

    return render(request, 'gestiongroupes/index.html', {"form": form})


def users_list(request):
    # Initialisation utilisateur
    current_user = init(request)
    if current_user == False:
        return HttpResponseRedirect('/')
    
    # Groupe plein
    message = ''
    if 'groupe_plein' in request.GET and request.GET['groupe_plein'] == '1':
        message = 'Le groupe est plein.'
    
    # Rejoint un groupe
    if request.method == 'POST':
        code = request.POST['code']
        return redirect('group_join', code)
    
    # Utilisateurs sans groupes
    users = Utilisateur.objects.filter(groupes=None)
    users_list = []
    for utilisateur in users:
        if utilisateur.nom != current_user.nom:
            users_list.append(utilisateur.nom)

    # Groupes joignables 
    groupes = Groupe.objects.annotate(num_utilisateurs=Count('utilisateurs')).filter(num_utilisateurs__gte=2)
    infos_groupes = []
    for groupe in groupes:
        infos_groupes.append({
            'id': groupe.id,
            'code': groupe.code,
            'nombre_membres': groupe.utilisateurs.count()
        })
    print(infos_groupes)
    # Fin
    context = {'users': users_list, 'infos_groupes':infos_groupes, 'message':message}
    return render(request, 'gestiongroupes/users_list.html', context)


def group_config(request):
    # Initialisation utilisateur
    current_user = init(request)
    if current_user == False:
        return HttpResponseRedirect('/')
    
    # On récupére la config des groupes
    config = get_group_config()

    form = GroupConfigForm()
    form.fields['max_users'].initial = config.max_users
    form.fields['max_groups'].initial = config.max_groups
    form.fields['last_group'].initial = config.last_group

    if request.method == 'POST':
        form = GroupConfigForm(request.POST)

        if form.is_valid():
            max_users = int(request.POST['max_users'])
            max_groups = int(request.POST['max_groups'])
            last_group = request.POST['last_group']

            config.max_users = max_users
            config.max_groups = max_groups
            config.last_group = last_group

            group_size, last_group_size = get_group_sizes(max_users, max_groups, last_group)

            config.group_size = group_size
            config.last_group_size = last_group_size

            config.save()

    return render(request, 'gestiongroupes/group_config.html', {"form": form, "config": config})


def group_details(request, group_id):
    # Initialisation utilisateur
    current_user = init(request)
    if current_user == False:
        return HttpResponseRedirect('/')
    
    # Initialisation groupe
    try:
        groupe = Groupe.objects.get(id=group_id)
        members = list(groupe.utilisateurs.values_list('nom', flat=True))
        if current_user not in groupe.utilisateurs.all():
            return HttpResponseRedirect('/liste/')
    except (Utilisateur.DoesNotExist, Groupe.DoesNotExist):
        return HttpResponseRedirect('/liste/')

    # Quitter le groupe 
    if 'quit' in request.GET and request.GET['quit'] == '1':
        groupe.utilisateurs.remove(current_user)
        if groupe.utilisateurs.count() == 0:
            groupe.delete()
        return HttpResponseRedirect('/liste/')

    # Lien du groupe
    group_url = request.scheme + '://' + request.get_host() + '/join-groupe/' + groupe.code

    context = {'name': "Groupe : " + str(groupe.code), 'members': members, 'url':group_url}
    return render(request, 'gestiongroupes/group_details.html', context)


def group_create(request):
    # Initialisation utilisateur
    current_user = init(request)
    if current_user == False:
        return HttpResponseRedirect('/')
    
    # Création groupe
    groupe = Groupe.objects.create()
    groupe.utilisateurs.add(current_user)
    groupe.save()
    return redirect('group_join', groupe.code)

def group_join(request, group_code):
    groupe = Groupe.objects.get(code=group_code)

    # Initialisation utilisateur
    current_user = init(request)
    if current_user == False:
        return HttpResponseRedirect('/')

    # On vérifie s'il reste de la place dans le groupe
    config = get_group_config()
    max_size = config.group_size
    if(get_nb_group_with_max_members() >= config.max_groups-1):
        # On dépasse le nombre de groupe de taille max 
        max_size = config.last_group_size
    if(groupe.utilisateurs.count() >= max_size):
        print('groupe plein')
        return HttpResponseRedirect('/liste/?groupe_plein=1')
    else:
        # On ajoute au groupe
        groupe.utilisateurs.add(current_user)
        
    return redirect('group_details', groupe.id)
    