from django import forms
from django.db import models


# Create your models here.
class GroupConfig(models.Model):
    LAST_GROUP_CHOICES = [
        ('LAST_MAX', 'Plus grand'),
        ('LAST_MIN', 'Plus petit')
    ]

    max_users = models.IntegerField()
    max_groups = models.IntegerField()
    last_group = models.CharField(max_length=8, choices=LAST_GROUP_CHOICES)
