from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from urllib.parse import urlencode


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
        for user in self.users:
            user.save()
        return super().setUp()

    def test_view_get_is_200(self):
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


class TestRegistrationView(TestCase):

    def test_view_get_is_200(self):
        resp = self.client.get('/users/create/')
        self.assertEqual(resp.status_code, 200)

    def test_view_post_is_successful(self):
        user_data = {
            'first_name': 'Bob', 
            'last_name': 'WoW', 
            'username': 'wiku',
            'password1': 'Pukote74.',
            'password2': 'Pukote74.'
        }
        resp_create = self.client.post(
            reverse('create_user'),
            urlencode(user_data),
            content_type='application/x-www-form-urlencoded',
            follow=True
        )
        self.assertRedirects(resp_create, reverse('login'))

        message = list(resp_create.context.get('messages'))[0]
        self.assertEqual(message.tags, "success")

        resp_users = self.client.get(reverse('users'))
        context_users = resp_users.context['users'].values()[0]
        self.assertEquals(
            first=[
                context_users['username'],
                context_users['first_name'],
                context_users['last_name'],
            ],
            second=[
                user_data['username'],
                user_data['first_name'],
                user_data['last_name'],
            ]
        )


class TestUpdateUserView(TestCase):

    def setUp(self) -> None:
        user1 = User.objects.create(
            first_name='Bob', 
            last_name='WoW', 
            username='wiku', 
        )
        user1.set_password('Pukote74.')
        user1.save()

        user2 = User.objects.create(
            first_name='Rob', 
            last_name='Glo', 
            username='gl'
            )
        user2.set_password('Pukote77.')
        user2.save()

        self.new_data = {
            'first_name': 'Wat',
            'last_name': 'WAT',
            'username': 'wWw',
            'password1': 'Pukote904.',
            'password2': 'Pukote904.',
        }

        return super().setUp()
    

    def test_view_get_is_200_authenticated(self):
        self.client.login(
            username='wiku',
            password='Pukote74.'
        )
        resp = self.client.get('/users/1/update/')
        self.assertEqual(resp.status_code, 200)

    def test_view_post_is_successful_authenticated(self):
        self.client.login(
            username='wiku',
            password='Pukote74.'
        )
        resp = self.client.post(
            reverse('update_user', kwargs={'pk': 1}),
            urlencode(self.new_data),
            content_type='application/x-www-form-urlencoded',
            follow=True
        )
        self.assertRedirects(resp, reverse('users'))
        message = list(resp.context.get('messages'))[0]
        self.assertEqual(message.tags, "success")

    def test_view_get_wrong_user(self):
        self.client.login(
            username='wiku',
            password='Pukote74.'
        )
        resp = self.client.get('/users/2/update/', follow=True)
        self.assertRedirects(resp, reverse('users'))

        message = list(resp.context.get('messages'))[0]
        self.assertEqual(message.tags, "error")

    def test_view_post_wrong_user(self):
        self.client.login(
            username='wiku',
            password='Pukote74.'
        )
        resp = self.client.post(
            reverse('update_user', kwargs={'pk': 2}),
            urlencode(self.new_data),
            content_type='application/x-www-form-urlencoded',
            follow=True
        )
        self.assertRedirects(resp, reverse('users'))

        message = list(resp.context.get('messages'))[0]
        self.assertEqual(message.tags, "error")

    def test_get_and_post_not_authenticated(self):
        resp = self.client.get('/users/1/update/', follow=True)
        self.assertRedirects(resp, reverse('login'))
        message = list(resp.context.get('messages'))[0]
        self.assertEqual(message.tags, "error")

        resp = self.client.post(
            reverse('update_user', kwargs={'pk': 1}),
            urlencode(self.new_data),
            content_type='application/x-www-form-urlencoded',
            follow=True
        )
        self.assertRedirects(resp, reverse('login'))
        message = list(resp.context.get('messages'))[0]
        self.assertEqual(message.tags, "error")

class TestDeleteUserView(TestCase):

    def setUp(self) -> None:
        user1 = User.objects.create(
            first_name='Bob', 
            last_name='WoW', 
            username='wiku', 
        )
        user1.set_password('Pukote74.')
        user1.save()

        user2 = User.objects.create(
            first_name='Rob', 
            last_name='Glo', 
            username='gl'
            )
        user2.set_password('Pukote77.')
        user2.save()

        self.new_data = {
            'first_name': 'Wat',
            'last_name': 'WAT',
            'username': 'wWw',
            'password1': 'Pukote904.',
            'password2': 'Pukote904.',
        }

        return super().setUp()

    def test_view_get_is_200_authenticated(self):
        self.client.login(
            username='wiku',
            password='Pukote74.'
        )
        resp = self.client.get('/users/1/delete/')
        self.assertEqual(resp.status_code, 200)

    def test_view_post_is_successful_authenticated(self):
        self.client.login(
            username='wiku',
            password='Pukote74.'
        )
        resp = self.client.post(
            reverse('delete_user', kwargs={'pk': 1}),
            content_type='application/x-www-form-urlencoded',
            follow=True
        )
        message = list(resp.context.get('messages'))[0]

        self.assertRedirects(resp, reverse('users'))
        self.assertEqual(message.tags, "success")

    def test_view_get_wrong_user(self):
        self.client.login(
            username='wiku',
            password='Pukote74.'
        )
        resp = self.client.get('/users/2/delete/', follow=True)
        message = list(resp.context.get('messages'))[0]

        self.assertRedirects(resp, reverse('users'))
        self.assertEqual(message.tags, "error")

    def test_view_post_wrong_user(self):
        self.client.login(
            username='wiku',
            password='Pukote74.'
        )
        resp = self.client.post(
            reverse('update_user', kwargs={'pk': 2}),
            content_type='application/x-www-form-urlencoded',
            follow=True
        )
        message = list(resp.context.get('messages'))[0]

        self.assertRedirects(resp, reverse('users'))
        self.assertEqual(message.tags, "error")

    def test_get_and_post_not_authenticated(self):
        resp = self.client.get('/users/1/delete/', follow=True)
        message = list(resp.context.get('messages'))[0]
        self.assertRedirects(resp, reverse('login'))
        self.assertEqual(message.tags, "error")

        resp = self.client.post(
            reverse('update_user', kwargs={'pk': 1}),
            urlencode(self.new_data),
            content_type='application/x-www-form-urlencoded',
            follow=True
        )
        message = list(resp.context.get('messages'))[0]
        self.assertRedirects(resp, reverse('login'))
        self.assertEqual(message.tags, "error")
