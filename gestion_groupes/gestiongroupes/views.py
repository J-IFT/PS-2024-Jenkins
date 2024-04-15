from math import floor, ceil
from random import random

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import ConnectionForm, GroupConfigForm
from .models import GroupConfig


def index(request):
    # session.get('username') plutôt que session['username'] pour éviter erreur si ['username'] n'existe pas encore
    if request.session.get('username'):
        if request.session['username'] == 'admin':
            return HttpResponseRedirect('/config/')

        return HttpResponseRedirect('/liste/')

    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            request.session['username'] = username
            if username == 'admin':
                return HttpResponseRedirect('/config/')

            return HttpResponseRedirect('/liste/')

    form = ConnectionForm()

    return render(request, 'gestiongroupes/index.html', {"form": form})


def users_list(request):
    if request.method == 'POST':
        join_id = request.POST['join_id']
        return redirect('group_details', join_id)

    context = {'users': ['Alice', 'Bob', 'Charlie']}
    return render(request, 'gestiongroupes/users_list.html', context)


def group_config(request):
    try:
        config = GroupConfig.objects.get(pk=1)
    except GroupConfig.DoesNotExist:
        config = GroupConfig()

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

            group_size, last_group_size = GroupConfig.get_group_sizes(max_users, max_groups, last_group)

            config.group_size = group_size
            config.last_group_size = last_group_size

            config.save()

    return render(request, 'gestiongroupes/group_config.html', {"form": form, "config": config})


def group_details(request, group_id):
    context = {'name': "Groupe " + str(group_id), 'members': ['Dylan', 'Eddy']}
    return render(request, 'gestiongroupes/group_details.html', context)


def group_create(request):
    # Vérification des groupes déjà existants
    # ID du nouveau groupe = dernier ID + 1
    group_id = floor(random() * 10)
    return redirect('group_details', group_id)
