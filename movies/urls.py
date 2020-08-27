from django.urls import path

from .views import MoviesListAPI, MoviesDetailAPI, WatchLaterListAPI, WatchedListAPI, WatchLaterDeleteApi, \
    WatchedListDeleteApi

urlpatterns = [
    path('list/', MoviesListAPI.as_view()),
    path('details/<int:pk>/', MoviesDetailAPI.as_view()),

    path('watchlater/', WatchLaterListAPI.as_view()),
    path('delete_from_watchlater/<int:movie_id>/', WatchLaterDeleteApi.as_view()),

    path('watched/', WatchedListAPI.as_view()),
    path('delete_from_watchedlist/<int:movie_id>/', WatchedListDeleteApi.as_view()),
]


