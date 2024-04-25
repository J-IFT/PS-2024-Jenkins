from django.test import TestCase

from .models import Groupe, GroupConfig, Utilisateur
from .tools import init, get_group_config, get_nb_group_with_max_members


class GroupConfigTestCase(TestCase):

    def test_get_group_sizes(self):
        """
        - Si le nombre d’utilisateurs est un multiple du nombre de groupes (ex : 20 utilisateurs et 5 groupes => 5 groupes de 4), ce paramètre n’a pas d’incidence.
        – Si la configuration vaut LAST_MIN, le dernier groupe a moins d’utilisateurs que les autres (ex : 19 utilisateurs et 5 groupes => 4 groupes de 4 et 1 groupe de 3)
        – Si la configuration vaut LAST_MAX, le dernier groupe a plus d’utilisateurs que les autres
        """

        self.assertEqual(GroupConfig.get_group_sizes(19, 5, 'LAST_MAX'), (3, 7))
        self.assertEqual(GroupConfig.get_group_sizes(20, 5, 'LAST_MAX'), (4, 4))
        self.assertEqual(GroupConfig.get_group_sizes(21, 5, 'LAST_MAX'), (4, 5))

        self.assertEqual(GroupConfig.get_group_sizes(19, 5, 'LAST_MIN'), (4, 3))
        self.assertEqual(GroupConfig.get_group_sizes(20, 5, 'LAST_MIN'), (4, 4))
        self.assertEqual(GroupConfig.get_group_sizes(21, 5, 'LAST_MIN'), (5, 1))


class ToolsTestCase(TestCase):
    def setUp(self):
        GroupConfig.objects.create(max_users=19, max_groups=5, last_group='LAST_MAX', group_size=3, last_group_size=7)

    def test_no_group_created(self):
        self.assertEqual(get_nb_group_with_max_members(), False)

    def test_no_maxed_out_group(self):
        self.group = Groupe.objects.create()
        self.group.utilisateurs.add(Utilisateur.objects.create(nom="Alice"))
        self.group.utilisateurs.add(Utilisateur.objects.create(nom="Bob"))
        self.group2 = Groupe.objects.create()
        self.group2.utilisateurs.add(Utilisateur.objects.create(nom="Charlie"))
        self.group2.utilisateurs.add(Utilisateur.objects.create(nom="Dave"))

        self.assertEqual(get_nb_group_with_max_members(), False)

    def test_maxed_out_small_group(self):
        self.group = Groupe.objects.create()
        self.group.utilisateurs.add(Utilisateur.objects.create(nom="Alice"))
        self.group.utilisateurs.add(Utilisateur.objects.create(nom="Bob"))
        self.group.utilisateurs.add(Utilisateur.objects.create(nom="Charlie"))

        self.assertEqual(get_nb_group_with_max_members(), 1)

        self.group2 = Groupe.objects.create()
        self.group2.utilisateurs.add(Utilisateur.objects.create(nom="Dave"))
        self.group2.utilisateurs.add(Utilisateur.objects.create(nom="Erin"))
        self.group2.utilisateurs.add(Utilisateur.objects.create(nom="Frank"))

        self.assertEqual(get_nb_group_with_max_members(), 2)

    def test_over_small_group_max(self):
        self.group = Groupe.objects.create()
        self.group.utilisateurs.add(Utilisateur.objects.create(nom="Alice"))
        self.group.utilisateurs.add(Utilisateur.objects.create(nom="Bob"))
        self.group.utilisateurs.add(Utilisateur.objects.create(nom="Charlie"))
        self.group.utilisateurs.add(Utilisateur.objects.create(nom="Dave"))

        self.assertEqual(get_nb_group_with_max_members(), False)
