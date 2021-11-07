from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from blog.models import Article
from blog.forms import AddPostForm


class BlogHomeView(ListView):
    model = Article
    template_name = 'blog/blog.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(is_published=True).order_by('-time_create')


class ArticleDetail(DetailView):
    model = Article
    template_name = 'blog/article.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'


class AddPost(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blog/add_post.html'
    success_url = reverse_lazy('blog')
    login_url = reverse_lazy('blog')
