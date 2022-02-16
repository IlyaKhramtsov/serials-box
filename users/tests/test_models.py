from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import Contact, Profile


class ContactModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name="test_user", email="test-user@mail.com", message="test message"
        )

    def test_contact_str(self):
        self.assertEqual(self.contact.__str__(), self.contact.email)


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.new_user = get_user_model().objects.create_user(
            "test_user", "username@mail.com"
        )
        cls.new_user.profile.birthday = date(2000, 1, 1)

    def test_create_profile(self):
        """
        Test that the profile is automatically created
        when an instance of the user class is created.
        """
        self.assertEqual(self.new_user.profile, Profile.objects.get(user=self.new_user))
        self.assertIsInstance(self.new_user.profile, Profile)
        self.assertEqual(Profile.objects.count(), 1)

    def test_user_age(self):
        """
        Test that the user's age is calculated correctly.
        """
        age = (date.today() - self.new_user.profile.birthday) // timedelta(
            days=365.2425
        )
        self.assertEqual(self.new_user.profile.get_age(), age)

    def test_profile_str_is_equal_to_username(self):
        self.assertEqual(self.new_user.profile.__str__(), self.new_user.username)
