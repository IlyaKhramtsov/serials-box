from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from serials.models import Category, Comment, TVSeries


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

    def test_view_uses_correct_template(self):
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


class SerialsDetailTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            name='test category',
            slug='test-category'
        )
        poster = SimpleUploadedFile('series_image.jpg', content=b'', content_type='image/jpg')
        cls.series = TVSeries.objects.create(
            title=f'Test series',
            description=f'Test series description',
            poster=poster,
            category=category,
            year=2001,
            slug=f'test-series'
        )
        cls.user = User.objects.create_user(
            username='test_user',
            password='12345'
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/series/test-series/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.series.get_absolute_url())
        self.assertTemplateUsed(response, 'serials/series_detail.html')

    def test_series_has_comment(self):
        Comment.objects.create(
            series=self.series,
            author=self.user,
            text='Test comment'
        )
        response = self.client.get(self.series.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test comment')