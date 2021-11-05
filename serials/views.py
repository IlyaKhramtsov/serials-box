from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, FormView

from serials.forms import CommentForm
from serials.models import TVSeries, Crew


class SerialsHomeView(ListView):
    """Show all serials."""
    paginate_by = 6
    model = TVSeries
    template_name = 'serials/index.html'
    context_object_name = 'serials'

    def get_queryset(self):
        return TVSeries.objects.filter(is_published=True).select_related('category')


class SeriesDetail(FormView, DetailView):
    """Shows information about the series."""
    model = TVSeries
    template_name = 'serials/series_detail.html'
    slug_url_kwarg = 'series_slug'
    context_object_name = 'series'
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.series = self.get_object()
        comment.author = self.request.user
        comment.save()
        return redirect(self.get_object().get_absolute_url())


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
        ).select_related('category')


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
