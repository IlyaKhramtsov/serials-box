from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        stuff = get_object_or_404(Article, slug=self.kwargs.get(self.slug_url_kwarg))
        total_likes = stuff.total_likes()
        context['total_likes'] = total_likes
        return context


class AddPostView(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blog/add_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AddPostView, self).form_valid(form)


def LikeView(request, slug):
    article = get_object_or_404(Article, slug=request.POST.get('article_slug'))
    article.likes.add(request.user)
    return HttpResponseRedirect(reverse('article_detail', args=[str(slug)]))
