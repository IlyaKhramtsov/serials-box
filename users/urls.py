from django.urls import path

from users.views import ContactFormView, LoginUser, UserRegisterView, ProfileEditView, UserProfileView, logout_user, UserEditView

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('edit_profile/<int:pk>/', ProfileEditView.as_view(), name='edit_profile'),
    path('edit_user/<int:pk>/', UserEditView.as_view(), name='edit_user'),
]
