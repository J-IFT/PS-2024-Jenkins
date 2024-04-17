from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('liste/', views.users_list, name='users_list'),
    path('config/', views.group_config, name='group_config'),
    path('details/<int:group_id>/', views.group_details, name='group_details'),
    path('creer-groupe/', views.group_create, name='group_create'),
    path('join-groupe/<int:group_id>/', views.group_join, name='group_join'),
]