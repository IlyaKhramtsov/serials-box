from django.urls import path

from blog.views import BlogHomeView, ArticleDetail, AddArticleView, UpdateArticleView, DeleteArticleView,LikeView

urlpatterns = [
    path('', BlogHomeView.as_view(), name='blog'),
    path('article/<slug:article_slug>/', ArticleDetail.as_view(), name='article_detail'),
    path('add_article/', AddArticleView.as_view(), name='add_article'),
    path('article/edit/<slug:slug>/', UpdateArticleView.as_view(), name='update_article'),
    path('article/<slug:slug>/delete/', DeleteArticleView.as_view(), name='delete_article'),
    path('like/<slug:slug>/', LikeView, name='like_article'),
]
