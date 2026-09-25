from django.db.models import Avg
from django.shortcuts import get_object_or_404, render

from .models import Genre, Movie


def recommendations(request, genre_id=None):
    """Public view: movies of the same genre ordered by best rating."""
    genres = Genre.objects.all()
    genre = None
    movies = Movie.objects.none()

    if genre_id:
        genre = get_object_or_404(Genre, pk=genre_id)
        movies = (
            Movie.objects.filter(genres=genre)
            .annotate(average=Avg("ratings__score"))
            .order_by("-average", "-year")
        )
    elif genres.exists():
        genre = genres.first()
        movies = (
            Movie.objects.filter(genres=genre)
            .annotate(average=Avg("ratings__score"))
            .order_by("-average", "-year")
        )

    return render(
        request,
        "movies/recommendations.html",
        {"genre": genre, "genres": genres, "movies": movies},
    )
