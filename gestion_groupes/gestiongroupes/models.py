from django.db import models


# Create your models here.
class GroupConfig(models.Model):
    LAST_GROUP_CHOICES = [
        ('LAST_MAX', 'Plus grand'),
        ('LAST_MIN', 'Plus petit')
    ]

    max_users = models.IntegerField(default=25)
    max_groups = models.IntegerField(default=5)
    last_group = models.CharField(max_length=8, choices=LAST_GROUP_CHOICES, default=LAST_GROUP_CHOICES[0][0])
