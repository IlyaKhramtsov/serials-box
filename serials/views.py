from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, FormView

from serials.forms import CommentForm
from serials.models import TVSeries, Crew


class SerialsHomeView(ListView):
    paginate_by = 6
    model = TVSeries
    template_name = 'serials/index.html'
    context_object_name = 'serials'

    def get_queryset(self):
        return TVSeries.objects.filter(is_published=True).select_related('category')


class SeriesDetail(FormView, DetailView):
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
    model = Crew
    template_name = 'serials/crew_detail.html'
    slug_url_kwarg = 'crew_slug'
    context_object_name = 'crew'
