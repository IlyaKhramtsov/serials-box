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
        response = self.client.get(f'/users/edit_user/{self.user.pk}/')

        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        url = reverse('edit_user', kwargs={'pk': self.user.pk})
        response = self.client.get(url)

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

    def test_authenticated_user_but_not_owner_can_not_see_page(self):
        not_owner = User.objects.create_user('test_user', 'strongpassword')
        self.client.force_login(user=not_owner)
        url = reverse('edit_user', kwargs={'pk': self.user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

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


class LoginUserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user1', password='12345')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/login/')

        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_user(self):
        data = {
            'username': 'user1',
            'password': '12345',
        }
        response = self.client.post(reverse('login'), data=data, follow=True)

        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.context['user'].is_active)


class UserProfileViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user1', password='12345')

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get(f'/users/profile/{self.user.username}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        url = reverse('profile', kwargs={'slug': self.user.username})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        url = reverse('profile', kwargs={'slug': self.user.username})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'users/user_profile.html')
