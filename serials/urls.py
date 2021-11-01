from django.urls import path

from serials.views import CrewDetail, SerialsHomeView, SerialsCategory, SeriesDetail, about

urlpatterns = [
    path('', SerialsHomeView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('series/<slug:series_slug>/', SeriesDetail.as_view(), name='series_detail'),
    path('category/<slug:category_slug>/', SerialsCategory.as_view(), name='category'),
    path('crew/<slug:crew_slug>/', CrewDetail.as_view(), name='crew_detail'),
]
