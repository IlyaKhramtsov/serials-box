from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from serials.models import Category, TVSeries


class SerialsHomeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            name='test category',
            slug='test-category'
        )
        poster = SimpleUploadedFile('series_image.jpg', content=b'', content_type='image/jpg')
        number_of_serials = 10
        for series_num in range(number_of_serials):
            TVSeries.objects.create(
                title=f'Test{series_num}',
                description=f'Test{series_num} description',
                poster=poster,
                category=category,
                year=2001,
                slug=f'test{series_num}'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'serials/index.html')

    def test_pagination_is_six(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(response.context['serials'].count(), 6)

    def test_next_page_pagination(self):
        """Test second page and confirm it has (exactly) remaining 4 items"""
        response = self.client.get(reverse('home') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(response.context['serials'].count(), 4)