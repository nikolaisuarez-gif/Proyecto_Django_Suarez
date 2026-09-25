from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    """Movie genre, related to movies with a many-to-many relation."""

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


class Person(models.Model):
    """Director or actor of a movie."""

    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=60, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Movie(models.Model):
    """Movie with genres (many-to-many) and ratings (foreign key)."""

    title = models.CharField(max_length=150)
    year = models.PositiveSmallIntegerField()
    synopsis = models.TextField(blank=True)
    poster = models.ImageField(upload_to="posters/", blank=True)
    director = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="directed_movies",
    )
    genres = models.ManyToManyField(Genre, related_name="movies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year", "title"]

    def __str__(self):
        return f"{self.title} ({self.year})"

    def average_rating(self):
        """Average score of the movie ratings, 0 when there are none."""
        ratings = self.ratings.all()
        if not ratings:
            return 0
        return round(sum(r.score for r in ratings) / len(ratings), 1)


class Rating(models.Model):
    """Score given by a user to a movie (foreign key to Movie)."""

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-score"]

    def __str__(self):
        return f"{self.movie.title} - {self.score}/10"
