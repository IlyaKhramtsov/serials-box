from django.urls import path

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

urlpatterns = [
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("contact/", ContactFormView.as_view(), name="contact"),
    path("profile/<str:slug>/", UserProfileView.as_view(), name="profile"),
    path("edit_profile/<str:slug>/", ProfileEditView.as_view(), name="edit_profile"),
    path("edit_user/<int:pk>/", UserEditView.as_view(), name="edit_user"),
    path("favorites/", UserFavoriteSerials.as_view(), name="favorites"),
    path("likes/", UserLikedArticles.as_view(), name="liked_articles"),
]
