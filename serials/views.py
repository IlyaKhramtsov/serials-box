from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, View

from serials.forms import CommentForm
from serials.models import Crew, TVSeries


class SerialsHomeView(ListView):
    """Show all serials."""
    paginate_by = 6
    model = TVSeries
    template_name = 'serials/index.html'
    context_object_name = 'serials'

    def get_queryset(self):
        return (
            TVSeries.objects
            .filter(is_published=True)
            .select_related('category')
            .prefetch_related('comments')
        )


class SeriesDetail(DetailView):
    """Shows information about the series."""

    queryset = TVSeries.objects.prefetch_related('comments__author__profile')
    template_name = 'serials/series_detail.html'
    slug_url_kwarg = 'series_slug'
    context_object_name = 'series'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['is_favorite'] = self.object.favorite.filter(id=self.request.user.id).exists()
        return context


class AddCommentView(CreateView):
    form_class = CommentForm
    template_name = 'serials/series_detail.html'

    def form_valid(self, form):
        form.instance.series = get_object_or_404(TVSeries, pk=self.kwargs.get('pk'))
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('series_detail', args=[self.object.series.slug])


class SerialsCategory(ListView):
    """Show TV series by category."""
    paginate_by = 6
    model = TVSeries
    template_name = 'serials/index.html'
    context_object_name = 'serials'

    def get_queryset(self):
        return TVSeries.objects.filter(
            category__slug=self.kwargs['category_slug'],
            is_published=True
        ).select_related('category').prefetch_related('comments')


class CrewDetail(DetailView):
    """Show information about the directors and actors of the series."""
    model = Crew
    template_name = 'serials/crew_detail.html'
    slug_url_kwarg = 'crew_slug'
    context_object_name = 'crew'


class SearchView(ListView):
    """Search TV series by title."""
    template_name = 'serials/index.html'
    context_object_name = 'serials'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return TVSeries.objects.filter(title__icontains=query)


class AddFavoriteView(View):
    """Add series to favorites."""
    def post(self, request, slug, *args, **kwargs):
        series = TVSeries.objects.get(slug=request.POST.get('series_slug'))
        series.favorite.add(request.user)
        return HttpResponseRedirect(reverse('series_detail', args=[str(slug)]))


class RemoveFavoriteView(View):
    """Remove series from favorites."""
    def post(self, request, slug, *args, **kwargs):
        series = TVSeries.objects.get(slug=request.POST.get('series_slug'))
        series.favorite.remove(request.user)
        return HttpResponseRedirect(reverse('series_detail', args=[str(slug)]))
