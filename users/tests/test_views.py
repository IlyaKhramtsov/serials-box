from django.test import TestCase, Client
from django.urls import reverse


class UserRegisterViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        client = Client()
        url = reverse('register')
        cls.response = client.get(url)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/users/register/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'users/register.html')
