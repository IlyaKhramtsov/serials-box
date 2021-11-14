from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from blog.models import Article
from blog.forms import AddPostForm
from blog.permissions import AdminAuthorPermissionMixin


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
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['total_likes'] = total_likes
        context['liked'] = liked
        return context


class AddArticleView(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blog/add_article.html'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateArticleView(LoginRequiredMixin, AdminAuthorPermissionMixin, UpdateView):
    model = Article
    form_class = AddPostForm
    template_name = 'blog/update_article.html'
    login_url = 'login'


class DeleteArticleView(LoginRequiredMixin, AdminAuthorPermissionMixin, DeleteView):
    model = Article
    template_name = 'blog/delete_article.html'
    success_url = reverse_lazy('blog')
    login_url = 'login'


def LikeView(request, slug):
    article = get_object_or_404(Article, slug=request.POST.get('article_slug'))
    liked = False
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('article_detail', args=[str(slug)]))
