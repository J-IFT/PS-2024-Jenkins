import uuid

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
    group_size = models.IntegerField(default=5)
    last_group_size = models.IntegerField(default=5)

    @staticmethod
    def get_group_sizes(max_users, max_groups, last_group):
        base_size = max_users // max_groups
        remainder = max_users % max_groups
        last_group_size = base_size + remainder

        if remainder != 0 and last_group == 'LAST_MIN':
            return base_size + 1, last_group_size - (max_groups - 1)

        return base_size, last_group_size


class Groupe(models.Model):
    id = models.AutoField(primary_key=True)
    utilisateurs = models.ManyToManyField('Utilisateur', related_name='groupes')
    code = models.CharField(max_length=4, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = uuid.uuid4().hex[:4].upper()
        super(Groupe, self).save(*args, **kwargs)


class Utilisateur(models.Model):
    nom = models.CharField(max_length=40)
