from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .forms import ConnectionForm, GroupConfigForm
from .models import GroupConfig


def index(request):
    if request.session.get('username'):
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
            config.max_users = request.POST['max_users']
            config.max_groups = request.POST['max_groups']
            config.last_group = request.POST['last_group']
            config.save()

    return render(request, 'gestiongroupes/group_config.html', {"form": form})


def group_details(request, group_id):
    context = {'name': "Groupe " + str(group_id), 'members': ['Dylan', 'Eddy']}
    return render(request, 'gestiongroupes/group_details.html', context)
