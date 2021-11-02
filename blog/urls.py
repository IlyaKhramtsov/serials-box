from django.urls import path

from blog.views import BlogHomeView

urlpatterns = [
    path('', BlogHomeView.as_view(), name='blog'),
]
