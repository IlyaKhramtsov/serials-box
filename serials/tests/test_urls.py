from django.test import SimpleTestCase
from django.urls import reverse, resolve
from serials.views import (
    AddCommentView,
    AddFavoriteView,
    CrewDetail,
    RemoveFavoriteView,
    SearchView,
    SerialsCategory,
    SerialsHomeView,
    SeriesDetail,
)


class TestSerialsUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, SerialsHomeView)

    def test_series_detail_url_is_resolved(self):
        url = reverse('series_detail', kwargs={'series_slug': 'test-series'})
        self.assertEquals(resolve(url).func.view_class, SeriesDetail)

    def test_category_url_is_resolved(self):
        url = reverse('category', kwargs={'category_slug': 'test-category'})
        self.assertEquals(resolve(url).func.view_class, SerialsCategory)

    def test_crew_detail_url_is_resolved(self):
        url = reverse('crew_detail', kwargs={'crew_slug': 'test-actor'})
        self.assertEquals(resolve(url).func.view_class, CrewDetail)

    def test_search_is_resolved(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func.view_class, SearchView)

    def test_comment_url_is_resolved(self):
        url = reverse('add_comment', kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, AddCommentView)

    def test_add_favorite_url_is_resolved(self):
        url = reverse('add_favorite', kwargs={'slug': 'test-series'})
        self.assertEquals(resolve(url).func.view_class, AddFavoriteView)

    def test_remove_favorite_url_is_resolved(self):
        url = reverse('remove_favorite', kwargs={'slug': 'test-series'})
        self.assertEquals(resolve(url).func.view_class, RemoveFavoriteView)
