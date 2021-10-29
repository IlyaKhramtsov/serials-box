from django.urls import path

from serials.views import SerialsHomeView, SerialsCategory, SeriesDetail, about, contact, login

urlpatterns = [
    path('', SerialsHomeView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('series/<slug:series_slug>/', SeriesDetail.as_view(), name='series_detail'),
    path('category/<slug:category_slug>/', SerialsCategory.as_view(), name='category'),
]
