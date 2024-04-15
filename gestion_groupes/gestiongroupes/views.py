from django.shortcuts import render

def index(request):
    return render(request, 'gestiongroupes/index.html')