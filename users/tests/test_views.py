import datetime

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.utils import override_settings
from django.test import TestCase
from django.urls import reverse

from blog.models import Article
from serials.models import Category, TVSeries
from users.models import Contact, Profile


@override_settings(AUTHENTICATION_BACKENDS=
                   ('django.contrib.auth.backends.ModelBackend',))
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

        self.assertEqual(User.objects.count(), 1)
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


class LogoutUserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user1', password='12345')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/logout/')

        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 302)

    def test_login_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'), follow=True)

        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)


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


class ProfileEditViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user1', password='12345')

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get(f'/users/edit_profile/{self.user.username}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        url = reverse('edit_profile', kwargs={'slug': self.user.username})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        url = reverse('edit_profile', kwargs={'slug': self.user.username})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'users/edit_profile.html')

    def test_update_user_profile(self):
        self.client.force_login(self.user)
        profile = Profile.objects.get(user=self.user)
        data = {
            'birthday': '2020-01-01',
            'city': 'Moscow'
        }
        url = reverse('edit_profile', kwargs={'slug': self.user.username})
        response = self.client.post(url, data=data)
        profile.refresh_from_db()

        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(profile.birthday, datetime.date(2020, 1, 1))
        self.assertEqual(profile.city, 'Moscow')
        self.assertRedirects(response, reverse('home'))


class ContactFormViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/contact/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('contact'))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('contact'))

        self.assertTemplateUsed(response, 'users/contact.html')

    def test_can_send_message(self):
        data = {
            'name': 'John',
            'email': 'johnsmith@example.com',
            'message': 'test message',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED'
        }
        response = self.client.post(reverse('contact'), data=data, follow=True)

        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.last().message, 'test message')
        self.assertRedirects(response, reverse('home'))
        # Check that response has success message
        self.assertContains(response, 'success')
        self.assertContains(response, 'Форма успешно отправлена!')


class UserFavoriteSerialsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            name='test category',
            slug='test-category'
        )
        poster = SimpleUploadedFile(
            'series_image.jpg',
            content=b'',
            content_type='image/jpg'
        )
        cls.series = TVSeries.objects.create(
            title='Test series',
            description='Test series description',
            poster=poster,
            category=category,
            year=2001,
            slug='test-series'
        )
        cls.user = User.objects.create_user(username='user1', password='12345')

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get('/users/favorites/')

        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('favorites'))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('favorites'))

        self.assertTemplateUsed(response, 'users/favorite.html')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('favorites'))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/users/login/'))

    def test_user_has_serials_in_favorites(self):
        self.client.force_login(self.user)
        self.user.favorite.add(self.series)
        response = self.client.get(reverse('favorites'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.series.favorite.count(), 1)
        self.assertEqual(self.user.favorite.get(title='Test series'), self.series)


class UserLikedArticlesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        author = User.objects.create_user(username='articles_author', password='12345')
        photo = SimpleUploadedFile('article_image.jpg', content=b'', content_type='image/jpg')
        cls.article = Article.objects.create(
            title='Test article',
            slug='test-article',
            content='Test article description',
            photo=photo,
            author=author
        )
        cls.user = User.objects.create_user(username='user1', password='12345')

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get('/users/likes/')

        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('liked_articles'))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('liked_articles'))

        self.assertTemplateUsed(response, 'users/liked_articles.html')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('liked_articles'))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/users/login/'))

    def test_user_has_liked_articles(self):
        self.client.force_login(self.user)
        self.user.blog_articles.add(self.article)
        response = self.client.get(reverse('liked_articles'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.article.likes.count(), 1)
        self.assertEqual(self.user.blog_articles.get(title='Test article'), self.article)
