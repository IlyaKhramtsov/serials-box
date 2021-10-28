from django.http import HttpResponse
from django.shortcuts import render
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


def series_detail(request, series_id):
    return HttpResponse(f'Отображение сериала с id = {series_id}')


def show_category(request, category_id):
    serials = TVSeries.objects.filter(category_id=category_id)
    context = {
        'serials': serials,
    }
    return render(request, 'serials/index.html', context=context)
