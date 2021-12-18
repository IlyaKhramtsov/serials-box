import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from users.forms import (
    ChangeProfileForm,
    ChangeUserForm,
    ContactForm,
    LoginUserForm,
    RegisterUserForm,
)


class RegisterUserFormTest(TestCase):

    def test_form_valid_data(self):
        form = RegisterUserForm(data={
            'username': 'user',
            'email': 'user@example.com',
            'password1': 'userpassword1',
            'password2': 'userpassword1'
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form = RegisterUserForm(data={
            'username': 'user',
            'email': 'user@example.com',
            'password1': '',
            'password2': '1'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class LoginUserFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpassword1',
        )

    def test_form_valid_data(self):
        form = LoginUserForm(data={
            'username': 'user',
            'password': 'userpassword1',
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_password(self):
        form = LoginUserForm(data={
            'username': 'user',
            'password': 'invalidpassword'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class ChangeUserFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpassword1',
        )

    def test_form_valid_data(self):
        form = ChangeUserForm(
            instance=self.user,
            data={
                'username': 'user1',
                'first_name': 'John'
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(self.user.username, form.data['username'])

    def test_form_invalid_username(self):
        form = ChangeUserForm(
            instance=self.user,
            data={
                'username': '',
                'first_name': 'John'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertNotEqual(self.user.username, form.data['username'])
        self.assertEqual(len(form.errors), 1)


class ChangeProfileFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpassword1',
        )
        cls.profile = user.profile

    def test_form_valid_data(self):
        form = ChangeProfileForm(
            instance=self.profile,
            data={
                'birthday': datetime.date(2000, 12, 15),
                'city': 'Moscow'
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(self.profile.birthday, form.data['birthday'])
        self.assertEqual(self.profile.city, form.data['city'])


class ContactFormTest(TestCase):

    def test_form_valid_data(self):
        form = ContactForm(data={
            'name': 'John Brown',
            'email': 'brown@example.com',
            'message': 'Test message',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED'
        })
        self.assertTrue(form.is_valid())
