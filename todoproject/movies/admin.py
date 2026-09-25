from django.contrib import admin

from .models import Genre, Movie, Person, Rating


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "birth_date", "country")
    search_fields = ("name",)
    list_filter = ("country",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "director", "created_at")
    list_filter = ("genres", "year")
    search_fields = ("title",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("movie", "score", "comment")
    list_filter = ("score",)
    search_fields = ("movie__title", "comment")
