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


class RatingInline(admin.TabularInline):
    """Ratings edited inside the movie form."""

    model = Rating
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "director", "created_at")
    list_filter = ("genres", "year")
    search_fields = ("title",)
    inlines = [RatingInline]
    readonly_fields = ("created_at", "updated_at")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("movie", "score", "comment")
    list_filter = ("score",)
    search_fields = ("movie__title", "comment")
    readonly_fields = ("created_at", "updated_at")
