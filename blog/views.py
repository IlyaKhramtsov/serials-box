from django.views.generic import DetailView, ListView

from blog.models import Article


class BlogHomeView(ListView):
    model = Article
    template_name = 'blog/blog.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


class ArticleDetail(DetailView):
    model = Article
    template_name = 'blog/article.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'
