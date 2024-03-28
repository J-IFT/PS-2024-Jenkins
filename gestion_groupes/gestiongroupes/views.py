from django.shortcuts import render


def index(request):
    return render(request, 'gestiongroupes/index.html')


def users_list(request):
    context = {'users': ['Alice', 'Bob', 'Charlie']}
    return render(request, 'gestiongroupes/users_list.html', context)


def group_config(request):
    return render(request, 'gestiongroupes/group_config.html')


def group_details(request, group_id):
    context = {'name': "Groupe " + str(group_id), 'members': ['Dylan', 'Eddy']}
    return render(request, 'gestiongroupes/group_details.html', context)
