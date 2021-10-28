from django.urls import path

from serials.views import SerialsHomeView, about, contact, login, series_detail, show_category

urlpatterns = [
    path('', SerialsHomeView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('series/<slug:series_slug>/', series_detail, name='series_detail'),
    path('category/<slug:category_slug>/', show_category, name='category'),
]
