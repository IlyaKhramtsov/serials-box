from django.urls import path

from blog.views import BlogHomeView, ArticleDetail, AddPost

urlpatterns = [
    path('', BlogHomeView.as_view(), name='blog'),
    path('article/<slug:article_slug>/', ArticleDetail.as_view(), name='article_detail'),
    path('add_post/', AddPost.as_view(), name='add_post'),
]
