from django.urls import path

from serials.views import SerialsHomeView

urlpatterns = [
    path('', SerialsHomeView.as_view(), name='home'),
]
