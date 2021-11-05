from django.urls import path

from serials.views import CrewDetail, SearchView, SerialsHomeView, SerialsCategory, SeriesDetail

urlpatterns = [
    path('', SerialsHomeView.as_view(), name='home'),
    path('series/<slug:series_slug>/', SeriesDetail.as_view(), name='series_detail'),
    path('category/<slug:category_slug>/', SerialsCategory.as_view(), name='category'),
    path('crew/<slug:crew_slug>/', CrewDetail.as_view(), name='crew_detail'),
    path('search/', SearchView.as_view(), name='search'),
]
