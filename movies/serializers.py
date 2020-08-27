from rest_framework.serializers import ModelSerializer

from movies.models import Movie, WatchLaterList


class MovieListSerializers(ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'featured_poster', 'imdb_source_url', 'imdb_rating', 'rating_user_count', 'created',
                  'modified')


class MovieDetailsSerializers(ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'featured_poster', 'imdb_source_url', 'imdb_rating', 'rating_user_count',
                  'created', 'modified')


class AddToWatchListSerializer(ModelSerializer):
    def create(self, validated_data):
        movie = validated_data.get('movie', None)
        user = self.context['request'].user

        watch_later_obj, created = WatchLaterList.objects.get_or_create(movie=movie, user=user)
        # Since it is for watch later list, therefore value of has_watched will be False
        watch_later_obj.has_watched = False
        watch_later_obj.save()
        return watch_later_obj

    class Meta:
        model = WatchLaterList
        fields = ('movie',)


class GetWatchListSerializer(ModelSerializer):
    movie = MovieListSerializers()

    class Meta:
        model = WatchLaterList
        fields = ('movie', 'has_watched', 'created')


class AddToWatchedListSerializer(ModelSerializer):
    def create(self, validated_data):
        movie = validated_data.get('movie', None)
        user = self.context['request'].user

        watch_later_obj, created = WatchLaterList.objects.get_or_create(movie=movie, user=user)
        # Since it is for watch later list, therefore value of has_watched will be False
        watch_later_obj.has_watched = True
        watch_later_obj.save()
        return watch_later_obj

    class Meta:
        model = WatchLaterList
        fields = ('movie',)


class GetWatchedListSerializer(ModelSerializer):
    movie = MovieListSerializers()

    class Meta:
        model = WatchLaterList
        fields = ('movie', 'has_watched', 'created')
