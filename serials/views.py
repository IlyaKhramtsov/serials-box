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
