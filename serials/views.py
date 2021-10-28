from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from serials.models import TVSeries


class SerialsHomeView(ListView):
    model = TVSeries
    template_name = 'serials/index.html'
    context_object_name = 'serials'

    def get_queryset(self):
        return TVSeries.objects.filter(is_published=True)


def about(request):
    return render(request, 'serials/about.html', {'title': 'О проекте'})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def series_detail(request, series_slug):
    series = get_object_or_404(TVSeries, slug=series_slug)
    context = {
        'series': series,
    }
    return render(request, 'serials/series_detail.html', context=context)


def show_category(request, category_slug):
    serials = TVSeries.objects.filter(category__slug=category_slug)
    context = {
        'serials': serials,
    }
    return render(request, 'serials/index.html', context=context)
