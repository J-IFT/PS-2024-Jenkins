from django.db import models

class Groupe(models.Model):
    id = models.AutoField(primary_key=True)

class Utilisateur(models.Model):
    nom = models.CharField(max_length=40)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
