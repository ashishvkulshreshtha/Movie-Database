import json
import os
import sys
from abc import ABC

import requests
from bs4 import BeautifulSoup
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from movies.models import Movie

'''
from utils.views import *
crawl_imdb("https://www.imdb.com/")

'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.8'
}


@api_view(["POST"])
def crawl_imdb(request):
    try:
        data = json.loads(request.body)
    except ValueError:
        return Response({"error": "Please provide `imdb_url` in POST body."}, status=status.HTTP_400_BAD_REQUEST)
    imdb_url = data.get("imdb_url", None)

    if not imdb_url:
        return Response({"error": "Please provide `imdb_url` in POST body."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        url = imdb_url
        r = requests.get(url, headers=headers)

        # Lets make the soup using html5lib
        list_soup = BeautifulSoup(r.content, 'html5lib')
        new_movie_count = 0
        existing_movie_count = 0
        error_count = 0
        for tr in list_soup.find('tbody', attrs={'class': 'lister-list'}).find_all('tr'):
            movie_dict = {}

            # Got an object of the Movie List
            # Fetching imdb_source_url from the movie object
            try:
                title_column = tr.find('td', attrs={'class': 'titleColumn'})
                imdb_source_url = "https://www.imdb.com" + title_column.a["href"]
                imdb_source_url = imdb_source_url.split("?")[0]

                movie_dict["imdb_source_url"] = imdb_source_url

                Movie.objects.get(imdb_source_url=movie_dict["imdb_source_url"])
                # If objects already exist ignore this Movie URL.
                existing_movie_count += 1

            except Movie.DoesNotExist:
                try:
                    with transaction.atomic():
                        tiny_featured_poster = tr.find('td', attrs={'class': 'posterColumn'}).a.img['src']
                        featured_poster = tiny_featured_poster.split("._V1_")
                        featured_poster[1] = "._V1_QL50_SY1000_CR0,0,675,1000_AL_.jpg"  # Replacing the size parameter
                        movie_dict['featured_poster'] = ''.join(featured_poster)
                        movie_dict["title"] = tr.find('td', attrs={'class': 'titleColumn'}).a.text
                        year = tr.find('td', attrs={'class': 'titleColumn'}).span.text
                        movie_dict["year"] = int(''.join(e for e in year if e.isdigit()))
                        rating = tr.find('td', attrs={'class': 'ratingColumn'}).strong.text
                        movie_dict["imdb_rating"] = float(rating)
                        rating_user_count = tr.find('td', attrs={'class': 'ratingColumn'}).strong["title"]
                        rating_user_count = rating_user_count.replace(rating, '')
                        movie_dict["rating_user_count"] = int(''.join(e for e in rating_user_count if e.isdigit()))
                        m_obj = Movie(**movie_dict)
                        m_obj.save()
                        new_movie_count += 1
                except Exception as e:
                    error_count += 1
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_tb.tb_lineno)
                    print(e)

        response_dict = {
            "new_movie_count": new_movie_count,
            "error_count": error_count,
            "existing_movie_count": existing_movie_count
        }
        return Response(response_dict, status=status.HTTP_201_CREATED)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error_message = "It seems given URL response can not be crawled. " + str(e) + ", Line Number: " + str(
            exc_tb.tb_lineno) + ", File Name: " + fname
        print(error_message)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
