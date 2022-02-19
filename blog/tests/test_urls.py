from django.test import SimpleTestCase
from django.urls import resolve, reverse

from blog.views import (
    AddArticleView,
    AddLikeView,
    ArticleDetail,
    BlogHomeView,
    DeleteArticleView,
    RemoveLikeView,
    UpdateArticleView,
)


class TestSerialsUrls(SimpleTestCase):
    def test_blog_url_is_resolved(self):
        url = reverse("blog")
        self.assertEquals(resolve(url).func.view_class, BlogHomeView)

    def test_article_detail_url_is_resolved(self):
        url = reverse("article_detail", kwargs={"article_slug": "test-article"})
        self.assertEquals(resolve(url).func.view_class, ArticleDetail)

    def test_add_article_is_resolved(self):
        url = reverse("add_article")
        self.assertEquals(resolve(url).func.view_class, AddArticleView)

    def test_update_article_url_is_resolved(self):
        url = reverse("update_article", kwargs={"slug": "test-article"})
        self.assertEquals(resolve(url).func.view_class, UpdateArticleView)

    def test_delete_article_url_is_resolved(self):
        url = reverse("delete_article", kwargs={"slug": "test-article"})
        self.assertEquals(resolve(url).func.view_class, DeleteArticleView)

    def test_add_like_url_is_resolved(self):
        url = reverse("add_like_article", kwargs={"slug": "test-article"})
        self.assertEquals(resolve(url).func.view_class, AddLikeView)

    def test_remove_like_url_is_resolved(self):
        url = reverse("remove_like_article", kwargs={"slug": "test-article"})
        self.assertEquals(resolve(url).func.view_class, RemoveLikeView)
