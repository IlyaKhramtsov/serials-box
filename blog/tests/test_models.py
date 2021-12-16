from django.contrib.auth import get_user_model
from django.test import TestCase

from blog.models import Article


class ArticleModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.new_user = get_user_model().objects.create_user(
            'test_user', 'username@mail.com')
        cls.article = Article.objects.create(
            title='New post',
            slug='new-post',
            content='Test new post content.',
            author=cls.new_user,
        )
        cls.article.likes.set([cls.new_user])

    def test_article_str_is_equal_to_title(self):
        self.assertEqual(self.article.__str__(), self.article.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.article.get_absolute_url(), '/blog/article/new-post/')

    def test_total_likes(self):
        self.assertEqual(self.article.total_likes(), 1)

    def test_user_liked_article(self):
        self.assertIn(self.new_user, self.article.likes.all())
