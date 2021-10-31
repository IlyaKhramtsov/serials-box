from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from serials.models import TVSeries, Crew


class SerialsHomeView(ListView):
    paginate_by = 6
    model = TVSeries
    template_name = 'serials/index.html'
    context_object_name = 'serials'

    def get_queryset(self):
        return TVSeries.objects.filter(is_published=True)


class SeriesDetail(DetailView):
    model = TVSeries
    template_name = 'serials/series_detail.html'
    slug_url_kwarg = 'series_slug'
    context_object_name = 'series'


class SerialsCategory(ListView):
    paginate_by = 6
    model = TVSeries
    template_name = 'serials/index.html'
    context_object_name = 'serials'

    def get_queryset(self):
        return TVSeries.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)


class CrewDetail(DetailView):
    model = Crew
    template_name = 'serials/crew_detail.html'
    slug_url_kwarg = 'crew_slug'
    context_object_name = 'crew'


def about(request):
    return render(request, 'serials/about.html', {'title': 'О проекте'})


def contact(request):
    return HttpResponse("Обратная связь")
