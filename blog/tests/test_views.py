from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from blog.models import Article


class BlogHomeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='user1', password='12345')
        photo = SimpleUploadedFile('article_image.jpg', content=b'', content_type='image/jpg')
        number_of_articles = 10
        for articles_num in range(number_of_articles):
            Article.objects.create(
                title=f'Article{articles_num}',
                slug=f'article{articles_num}',
                content=f'Article{articles_num} description',
                photo=photo,
                author=user
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blog'))
        self.assertTemplateUsed(response, 'blog/blog.html')

    def test_blog_contains_10_articles(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['articles'].count(), 10)


class ArticleDetailTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='user1', password='12345')
        photo = SimpleUploadedFile('article_image.jpg', content=b'', content_type='image/jpg')
        cls.article = Article.objects.create(
            title='Test article',
            slug='test-article',
            content='Test article description',
            photo=photo,
            author=user
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/article/test-article/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertTemplateUsed(response, 'blog/article.html')

    def test_redirect_to_article_after_adding_like(self):
        self.client.login(username='user1', password='12345')
        url = reverse('add_like_article', kwargs={'slug': self.article.slug})
        response = self.client.post(url, data={
            'article_slug': self.article.slug,
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.article.get_absolute_url())

    def test_redirect_to_article_after_removing_like(self):
        self.client.login(username='user1', password='12345')
        url = reverse('remove_like_article', kwargs={'slug': self.article.slug})
        response = self.client.post(url, data={
            'article_slug': self.article.slug,
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.article.get_absolute_url())


class AddArticleTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='user1', password='12345')

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.author)
        response = self.client.get('/blog/add_article/')

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('add_article'))

        self.assertTemplateUsed(response, 'blog/add_article.html')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('add_article'))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/users/login/'))

    def test_add_article(self):
        self.client.force_login(self.author)
        data = {
            'title': 'New article',
            'slug': 'new-article',
            'content': 'New article description.'
        }
        photo = {
            'photo': SimpleUploadedFile(
                'article_image.jpg',
                content=open('static/serials/images/avatar.png', 'rb').read(),
                content_type='image/jpg')
        }
        self.client.post(reverse('add_article'), data={**data, **photo})

        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.last().title, 'New article')


class DeleteArticleTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='user1', password='12345')
        photo = SimpleUploadedFile(
            'article_image.jpg',
            content=b'',
            content_type='image/jpg'
        )
        cls.article = Article.objects.create(
            title='Test article',
            slug='test-article',
            content='Test article description',
            photo=photo,
            author=cls.author
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.author)
        response = self.client.get('/blog/article/test-article/delete/')

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.author)
        url = reverse('delete_article', kwargs={'slug': self.article.slug})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'blog/delete_article.html')

    def test_redirect_if_not_logged_in(self):
        url = reverse('delete_article', kwargs={'slug': self.article.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/users/login/'))

    def test_delete_article(self):
        self.client.force_login(self.author)
        url = reverse('delete_article', kwargs={'slug': self.article.slug})
        response = self.client.delete(url)

        self.assertEquals(Article.objects.count(), 0)
        self.assertRedirects(response, reverse('blog'), status_code=302)


class ArticleUpdateTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='user1', password='12345')
        photo = SimpleUploadedFile(
            'article_image.jpg',
            content=open('static/serials/images/avatar.png', 'rb').read(),
            content_type='image/jpg'
        )
        cls.article = Article.objects.create(
            title='Test article',
            slug='test-article',
            content='Test article description',
            photo=photo,
            author=cls.author
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.author)
        response = self.client.get('/blog/article/edit/test-article/')

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.author)
        url = reverse('update_article', kwargs={'slug': self.article.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/update_article.html')

    def test_redirect_if_not_logged_in(self):
        url = reverse('update_article', kwargs={'slug': self.article.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/users/login/'))

    def test_update_article_content(self):
        self.client.force_login(self.author)
        data = {
            'title': self.article.title,
            'slug': self.article.slug,
            'content': 'updated content',
            'photo': self.article.photo
        }
        url = reverse('update_article', kwargs={'slug': self.article.slug})
        response = self.client.post(url, data=data)

        self.assertEquals(Article.objects.count(), 1)
        self.assertEqual(Article.objects.last().content, 'updated content')
        self.assertRedirects(response, self.article.get_absolute_url())
