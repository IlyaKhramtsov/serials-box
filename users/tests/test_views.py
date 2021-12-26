from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserRegisterViewTests(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_user(self):
        data = {
            'username': 'test-user',
            'email': 'user@example.com',
            'password1': 'userpassword1',
            'password2': 'userpassword1'
        }
        response = self.client.post(reverse('register'), data=data)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.last().username, 'test-user')
        self.assertRedirects(response, reverse('home'))


class UserEditViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user1', password='12345')

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get('/users/edit_user/1/')

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        url = reverse('edit_user', kwargs={'pk': self.user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit_user.html')

    def test_redirect_if_not_logged_in(self):
        url = reverse('edit_user', kwargs={'pk': self.user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/users/login/'))

    def test_update_user_credentials(self):
        self.client.force_login(self.user)
        data = {
            'username': 'upd_username',
            'first_name': 'John'
        }
        url = reverse('edit_user', kwargs={'pk': self.user.pk})
        response = self.client.post(url, data=data)

        self.assertEquals(User.objects.count(), 1)
        self.assertEqual(User.objects.last().username, 'upd_username')
        self.assertEqual(User.objects.last().first_name, 'John')
        self.assertRedirects(response, reverse('home'))
