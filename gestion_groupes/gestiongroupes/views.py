from math import floor, ceil
from random import random

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Count

from .forms import ConnectionForm, GroupConfigForm
from .models import GroupConfig, Groupe, Utilisateur

from .tools import init, get_group_config, get_nb_group_with_max_members


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
    if 'message' in request.GET:
        message = request.GET['message']

    # Rejoint un groupe
    if request.method == 'POST':
        code = request.POST['code']
        return redirect('group_join', code)

    # Utilisateurs sans groupes
    users = Utilisateur.objects.filter(groupes=None)
    users_list = []
    for utilisateur in users:
        if utilisateur.id != current_user.id:
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
    context = {'users': users_list, 'infos_groupes': infos_groupes, 'message': message, 'current_user': current_user}
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

    group_size, last_group_size = GroupConfig.get_group_sizes(config.max_users, config.max_groups, config.last_group)

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

    context = {'name': "Groupe : " + str(groupe.code), 'members': members, 'url': group_url}
    return render(request, 'gestiongroupes/group_details.html', context)


def group_create(request):
    # Initialisation utilisateur
    current_user = init(request)
    if current_user == False:
        return HttpResponseRedirect('/')

    # Check si le user n'est pas déjà dans un groupe
    if (current_user.groupes.exists()):
        return HttpResponseRedirect('/liste/?message=Déjà%20dans%20un%20groupe.')

    # Vérification avec la config
    config = get_group_config()
    if (Groupe.objects.count() >= config.max_groups):
        return HttpResponseRedirect('/liste/?message=Le%20nombre%20maximum%20de%20groupes%20à%20été%20atteint.')

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
    if (get_nb_group_with_max_members() >= config.max_groups - 1):
        # On dépasse le nombre de groupe de taille max
        max_size = config.last_group_size
    if (groupe.utilisateurs.count() >= max_size):
        print('groupe plein')
        return HttpResponseRedirect('/liste/?message=Le%20groupe%20est%20plein.')
    else:
        # On ajoute au groupe
        groupe.utilisateurs.add(current_user)

    return redirect('group_details', groupe.id)
