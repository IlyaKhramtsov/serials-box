from django.urls import path

from users.views import login, RegisterUser

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
]