from django.urls import path
from .views import crawl_imdb

urlpatterns = [
    path('crawl_imdb_list/', crawl_imdb),
]
