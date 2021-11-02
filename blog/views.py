from django.shortcuts import render
from django.views.generic import ListView

from blog.models import Article


class BlogHomeView(ListView):
    model = Article
    template_name = 'blog/blog.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(is_published=True)
