from django.contrib.auth import get_user_model
from django.test import TestCase

from serials.models import Category, Crew, Comment, Genre, TVSeries


class TVSeriesModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            'User1', 'user1@mail.com')

        cls.category = Category.objects.create(
            name='test category',
            slug='test-category'
        )

        cls.series = TVSeries.objects.create(
            title='Scrubs',
            description='Scrubs description',
            category=cls.category,
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
        self.assertEqual(self.series.actors.get(id=2).name, self.actor.name)
        self.assertEqual(self.series.directors.get(id=3).name, self.director.name)

    def test_serials_absolute_url(self):
        self.assertEqual(self.series.get_absolute_url(), '/series/scrubs/')

    def test_series_in_favorites(self):
        """Tests that the series is in the user's favorites."""
        self.series.favorite.add(self.user)

        self.assertTrue(self.series.favorite)
        self.assertEqual(self.user.favorite.get(title='Scrubs'), self.series)
        self.assertEqual(self.series.favorite.get(id=self.user.id), self.user)


class GenreModelTest(TestCase):

    def setUp(self):
        self.genre = Genre(name='Test genre', slug='test-genre')

    def test_genre_str_is_equal_to_name(self):
        self.assertEqual(self.genre.__str__(), self.genre.name)


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            'User1', 'user1@mail.com')

        category = Category.objects.create(
            name='test category',
            slug='test-category'
        )

        cls.series = TVSeries.objects.create(
            title='Test series',
            description='Test series description',
            category=category,
            year=2001,
            slug='test-series'
        )

        cls.comment = Comment.objects.create(
            series=cls.series,
            author=cls.user,
            text='The best series'
        )

    def test_comment_str(self):
        expected_str = f'Комментарий от {self.comment.author} на {self.comment.series}'
        self.assertEqual(self.comment.__str__(), expected_str)

    def test_comment_listing(self):
        self.assertEqual(self.user.comment_set.get(id=1).series, self.series)
        self.assertEqual(self.user.comment_set.get(id=1).text, 'The best series')
        self.assertEqual(self.comment.series.title, self.series.title)
        self.assertEqual(self.comment.author.username, self.user.username)


class CrewModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.crew = Crew.objects.create(name='test_actor', slug='test-actor')

    def test_crew_str_is_equal_to_name(self):
        self.assertEqual(self.crew.__str__(), self.crew.name)

    def test_serials_absolute_url(self):
        self.assertEqual(self.crew.get_absolute_url(), '/crew/test-actor/')
