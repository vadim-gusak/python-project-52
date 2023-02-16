from django.test import TestCase
from task_manager.views import UsersView
from django.contrib.auth.models import User
from django.urls import reverse


class TestUsersView(TestCase):

    def setUp(self) -> None:
        self.users = [
            User.objects.create(
                first_name='Bob', 
                last_name='WoW', 
                username='wiku', 
                is_staff=True
                ),
            User.objects.create(
                first_name='Rob', 
                last_name='Glo', 
                username='gl'
                ),
            User.objects.create(
                first_name='Uki', 
                last_name='G', 
                username='lovz'
                )
        ]
        return super().setUp()

    def test_view_is_200(self):
        resp = self.client.get('/users/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('users'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('users'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users.html')

    def test_lists_all_users(self):
        resp = self.client.get(reverse('users'))
        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(list(resp.context['users']), self.users[1:3])
