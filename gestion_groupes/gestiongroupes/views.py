from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ConnectionForm


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
    return render(request, 'gestiongroupes/group_config.html')


def group_details(request, group_id):
    context = {'name': "Groupe " + str(group_id), 'members': ['Dylan', 'Eddy']}
    return render(request, 'gestiongroupes/group_details.html', context)
