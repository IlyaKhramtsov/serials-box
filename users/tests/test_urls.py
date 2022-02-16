from django.test import SimpleTestCase
from django.urls import resolve, reverse

from users.views import (
    ContactFormView,
    LoginUser,
    ProfileEditView,
    UserEditView,
    UserFavoriteSerials,
    UserLikedArticles,
    UserProfileView,
    UserRegisterView,
    logout_user,
)


class TestUsersUrls(SimpleTestCase):
    def test_login_url_is_resolved(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func.view_class, LoginUser)

    def test_logout_url_is_resolved(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).func, logout_user)

    def test_register_url_is_resolved(self):
        url = reverse("register")
        self.assertEqual(resolve(url).func.view_class, UserRegisterView)

    def test_edit_user_url_is_resolved(self):
        url = reverse("edit_user", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, UserEditView)

    def test_profile_is_resolved(self):
        url = reverse("profile", kwargs={"slug": "username"})
        self.assertEqual(resolve(url).func.view_class, UserProfileView)

    def test_edit_profile_url_is_resolved(self):
        url = reverse("edit_profile", kwargs={"slug": "username"})
        self.assertEqual(resolve(url).func.view_class, ProfileEditView)

    def test_liked_articles_url_is_resolved(self):
        url = reverse("liked_articles")
        self.assertEqual(resolve(url).func.view_class, UserLikedArticles)

    def test_favorites_url_is_resolved(self):
        url = reverse("favorites")
        self.assertEqual(resolve(url).func.view_class, UserFavoriteSerials)

    def test_contact_url_is_resolved(self):
        url = reverse("contact")
        self.assertEqual(resolve(url).func.view_class, ContactFormView)
