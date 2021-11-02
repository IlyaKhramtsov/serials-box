from django.urls import path

from blog.views import BlogHomeView, ArticleDetail

urlpatterns = [
    path('', BlogHomeView.as_view(), name='blog'),
    path('article/<slug:article_slug>/', ArticleDetail.as_view(), name='article_detail'),
]
