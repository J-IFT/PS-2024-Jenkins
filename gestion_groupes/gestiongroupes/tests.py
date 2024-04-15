from django.test import TestCase
from gestiongroupes.models import GroupConfig


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
