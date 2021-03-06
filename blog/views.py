from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from blog.forms import AddPostForm
from blog.models import Article
from blog.permissions import AdminAuthorPermissionMixin


class BlogHomeView(ListView):
    """Show all articles."""

    model = Article
    template_name = "blog/blog.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(is_published=True).order_by("-time_create")


class ArticleDetail(DetailView):
    """Show the article."""

    queryset = Article.objects.select_related("author")
    template_name = "blog/article.html"
    slug_url_kwarg = "article_slug"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_liked"] = self.object.likes.filter(id=self.request.user.id).exists()
        context["total_likes"] = self.object.total_likes()
        return context


class AddArticleView(LoginRequiredMixin, CreateView):
    """Add a new article."""

    form_class = AddPostForm
    template_name = "blog/add_article.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateArticleView(LoginRequiredMixin, AdminAuthorPermissionMixin, UpdateView):
    """Update the article."""

    model = Article
    form_class = AddPostForm
    template_name = "blog/update_article.html"
    login_url = "login"


class DeleteArticleView(LoginRequiredMixin, AdminAuthorPermissionMixin, DeleteView):
    """Delete the article."""

    model = Article
    template_name = "blog/delete_article.html"
    success_url = reverse_lazy("blog")
    login_url = "login"


class AddLikeView(View):
    """Add a like to the article."""

    def post(self, request, slug, *args, **kwargs):
        article = Article.objects.get(slug=request.POST.get("article_slug"))
        article.likes.add(request.user)
        return HttpResponseRedirect(reverse("article_detail", args=[str(slug)]))


class RemoveLikeView(View):
    """Remove the like from the article."""

    def post(self, request, slug, *args, **kwargs):
        article = Article.objects.get(slug=request.POST.get("article_slug"))
        article.likes.remove(request.user)
        return HttpResponseRedirect(reverse("article_detail", args=[str(slug)]))
