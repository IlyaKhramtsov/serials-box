from django.urls import path

from users.views import ContactFormView, LoginUser, RegisterUser, UserProfileView, logout_user

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
]
