from django.contrib.auth import get_user_model
from django.test import TestCase

from serials.models import Category, Crew, Comment, Genre, TVSeries


class SerialsModelsTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'User1', 'user1@mail.com')

        self.category = Category.objects.create(
            name='test category',
            slug='test-category'
        )

        self.series = TVSeries.objects.create(
            title='Scrubs',
            description='Scrubs description',
            category=self.category,
            year=2001,
            slug='scrubs'
        )

    def test_series_listing(self):
        self.genre = Genre.objects.create(
            name='Comedy',
            slug='comedy'
        )
        self.actor = Crew.objects.create(
            name='Zach Braff',
            slug='zach-braff'
        )
        self.director = Crew.objects.create(
            name='Bill Lawrence',
            slug='bill-lawrence'
        )

        self.series.genres.add(self.genre)
        self.series.actors.add(self.actor)
        self.series.directors.add(self.director)

        self.assertEqual(self.series.title, 'Scrubs')
        self.assertEqual(self.series.description, 'Scrubs description')
        self.assertEqual(self.series.year, 2001)
        self.assertEqual(self.series.category.name, 'test category')
        self.assertEqual(self.series.genres.get(id=1).name, self.genre.name)
        self.assertEqual(self.series.actors.get(id=1).name, self.actor.name)
        self.assertEqual(self.series.directors.get(id=2).name, self.director.name)

    def test_serials_absolute_url(self):
        self.assertEqual(self.series.get_absolute_url(), '/series/scrubs/')

    def test_comment_model(self):
        comment = Comment.objects.create(
            series=self.series,
            author=self.user,
            text='The best series'
        )

        self.assertEqual(self.user.comment_set.get(id=1).series, self.series)
        self.assertEqual(self.user.comment_set.get(id=1).text, 'The best series')
        self.assertEqual(comment.series.title, self.series.title)
        self.assertEqual(comment.author.username, self.user.username)

    def test_series_in_favorites(self):
        """Tests that the series is in the user's favorites."""
        self.series.favorite.add(self.user)

        self.assertTrue(self.series.favorite)
        self.assertEqual(self.user.favorite.get(title='Scrubs'), self.series)
        self.assertEqual(self.series.favorite.get(id=self.user.id), self.user)
