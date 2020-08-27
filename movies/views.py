from django.db import transaction
from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from movies.models import Movie, WatchLaterList
from movies.serializers import MovieListSerializers, MovieDetailsSerializers, AddToWatchListSerializer, \
    GetWatchListSerializer, AddToWatchedListSerializer, GetWatchedListSerializer


# As per the problem statement all the users (Anonymous and loggedIn) can see the list of the movies
class MoviesListAPI(ListAPIView):
    serializer_class = MovieListSerializers

    def get_queryset(self):
        qs = Movie.objects.all().order_by('-id')
        search_query = self.request.GET.get('q', None)

        if search_query:
            # If URL having a search query parameter
            qs = qs.filter(title__icontains=search_query)
        return qs


# As per the problem statement all the users (Anonymous and loggedIn) can see the details of the movies
class MoviesDetailAPI(RetrieveAPIView):
    serializer_class = MovieDetailsSerializers
    queryset = Movie.objects.all()


# This API will handle the `Watch later` creation and listing part,
class WatchLaterListAPI(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddToWatchListSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetWatchListSerializer
        return AddToWatchListSerializer

    def get_serializer_context(self):
        # passing the `request` through `context` to the serializer to fetch user information in serializer class.
        context = super(WatchLaterListAPI, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    headers = self.get_success_headers(serializer.data)
                    response_data = serializer.data
                    response_data["message"] = "Successfully added to your Watch later list."
                    return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        # Here user = request.user, it means a user can see only his Watchlater list.
        qs = WatchLaterList.objects.filter(user=self.request.user).order_by('-id')
        # Showing only watch later list where has_watched = False
        qs = qs.filter(has_watched=False)
        return qs


class WatchLaterDeleteApi(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        movie_id = self.kwargs.get('movie_id')
        try:
            return WatchLaterList.objects.get(movie_id=movie_id, user=self.request.user, has_watched=False)
        except WatchLaterList.DoesNotExist:
            raise Http404


#########################################################################
# This API will handle the `WatchedList` creation and listing part,
class WatchedListAPI(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddToWatchedListSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetWatchedListSerializer
        return AddToWatchedListSerializer

    def get_serializer_context(self):
        # passing the `request` through `context` to the serializer to fetch user information in serializer class.
        context = super(WatchedListAPI, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    headers = self.get_success_headers(serializer.data)
                    response_data = serializer.data
                    response_data["message"] = "Successfully added to your Watched list."
                    return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        # Here user = request.user, it means a user can see only his Watchlater list.
        qs = WatchLaterList.objects.filter(user=self.request.user).order_by('-id')
        # Showing only watch later list where has_watched = False
        qs = qs.filter(has_watched=True)
        return qs


class WatchedListDeleteApi(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        movie_id = self.kwargs.get('movie_id')
        try:
            return WatchLaterList.objects.get(movie_id=movie_id, user=self.request.user, has_watched=True)
        except WatchLaterList.DoesNotExist:
            raise Http404
