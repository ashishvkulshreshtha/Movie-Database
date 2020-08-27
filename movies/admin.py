from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Movie, WatchLaterList


class MovieAdmin(admin.ModelAdmin):
    def poster_tag(self, obj):
        return mark_safe('<img src="%s" width="120" />' % obj.featured_poster)

    poster_tag.short_description = 'Poster Preview'

    def rating_tag(self, obj):
        return mark_safe(
            '<img src="data:image/svg+xml;base64, PHN2ZyB3aWR0aD0iMzAiIGhlaWdodD0iMjgiIHZpZXdCb3g9IjAgMCAzMCAyOCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTE1LjAwMjQgMEwxOC4zNzAyIDEwLjM2NDdIMjkuMjY4M0wyMC40NTE1IDE2Ljc3MDVMMjMuODE5MiAyNy4xMzUzTDE1LjAwMjQgMjAuNzI5NUw2LjE4NTY2IDI3LjEzNTNMOS41NTMzNyAxNi43NzA1TDAuNzM2NTkzIDEwLjM2NDdIMTEuNjM0N0wxNS4wMDI0IDBaIiBmaWxsPSIjRTA5QjNEIi8+Cjwvc3ZnPg==" width="20" /> %s' % obj.imdb_rating)

    rating_tag.short_description = 'IMDB Rating'

    readonly_fields = ('poster_tag', 'rating_tag')
    list_display = ('id', 'poster_tag', '__str__', 'rating_tag', 'rating_user_count')
    search_fields = ('title',)
    list_filter = ('imdb_rating',)


admin.site.register(Movie, MovieAdmin)


class WatchLaterListAdmin(admin.ModelAdmin):
    def poster_tag(self, obj):
        return mark_safe('<img src="%s" width="75" />' % obj.movie.featured_poster)

    poster_tag.short_description = 'Poster Preview'

    def has_change_permission(self, request, obj=None):
        # All field should be readonly and can not edit via admin panel.
        return False

    list_display = ('user', 'poster_tag', 'movie', 'has_watched', 'created',)
    list_filter = ('has_watched',)


admin.site.register(WatchLaterList, WatchLaterListAdmin)
