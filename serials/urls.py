from django.urls import path

from serials.views import (
    AddCommentView,
    AddFavoriteView,
    Categories,
    CrewDetail,
    RemoveFavoriteView,
    SearchView,
    SerialsCategory,
    SerialsHomeView,
    SeriesDetail,
)

urlpatterns = [
    path('', SerialsHomeView.as_view(), name='home'),
    path('series/<slug:series_slug>/', SeriesDetail.as_view(), name='series_detail'),
    path('category/<slug:category_slug>/', SerialsCategory.as_view(), name='category'),
    path('categories/', Categories.as_view(), name='categories'),
    path('crew/<slug:crew_slug>/', CrewDetail.as_view(), name='crew_detail'),
    path('search/', SearchView.as_view(), name='search'),
    path('comment/<int:pk>/', AddCommentView.as_view(), name='add_comment'),
    path('favorite/add/<slug:slug>/', AddFavoriteView.as_view(), name='add_favorite'),
    path('favorite/remove/<slug:slug>/', RemoveFavoriteView.as_view(), name='remove_favorite'),
]
