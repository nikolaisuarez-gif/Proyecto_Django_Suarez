from django.core.management.base import BaseCommand

from movies.models import Genre, Movie, Person, Rating


class Command(BaseCommand):
    help = "Seed: 4 genres, 10 movies and ratings for 6 of them."

    def handle(self, *args, **options):
        action, _ = Genre.objects.get_or_create(
            name="Action", defaults={"description": "Stunts, fights and fast pace."}
        )
        drama, _ = Genre.objects.get_or_create(
            name="Drama", defaults={"description": "Emotional stories about people."}
        )
        comedy, _ = Genre.objects.get_or_create(
            name="Comedy", defaults={"description": "Movies to laugh about."}
        )
        scifi, _ = Genre.objects.get_or_create(
            name="Sci-Fi", defaults={"description": "Science fiction and the future."}
        )

        nolan, _ = Person.objects.get_or_create(
            name="Christopher Nolan", defaults={"country": "United Kingdom"}
        )
        villeneuve, _ = Person.objects.get_or_create(
            name="Denis Villeneuve", defaults={"country": "Canada"}
        )
        gerwig, _ = Person.objects.get_or_create(
            name="Greta Gerwig", defaults={"country": "United States"}
        )
        coppola, _ = Person.objects.get_or_create(
            name="Francis Ford Coppola", defaults={"country": "United States"}
        )

        movies = [
            {"title": "The Dark Knight", "year": 2008, "director": nolan, "genres": [action, drama]},
            {"title": "Inception", "year": 2010, "director": nolan, "genres": [action, scifi]},
            {"title": "Interstellar", "year": 2014, "director": nolan, "genres": [scifi, drama]},
            {"title": "Dune", "year": 2021, "director": villeneuve, "genres": [scifi, action]},
            {"title": "Blade Runner 2049", "year": 2017, "director": villeneuve, "genres": [scifi, drama]},
            {"title": "Little Women", "year": 2019, "director": gerwig, "genres": [drama]},
            {"title": "Barbie", "year": 2023, "director": gerwig, "genres": [comedy]},
            {"title": "The Godfather", "year": 1972, "director": coppola, "genres": [drama]},
            {"title": "The Breakfast Club", "year": 1985, "director": None, "genres": [comedy, drama]},
            {"title": "Mad Max: Fury Road", "year": 2015, "director": None, "genres": [action]},
        ]

        for data in movies:
            movie, _ = Movie.objects.get_or_create(
                title=data["title"],
                year=data["year"],
                defaults={"director": data["director"], "synopsis": ""},
            )
            movie.genres.set(data["genres"])

        ratings = [
            ("The Dark Knight", 9, "Best Batman movie."),
            ("Inception", 8, "Great ideas and ending."),
            ("Interstellar", 9, "Emotional and smart."),
            ("Dune", 8, "Amazing visuals."),
            ("Blade Runner 2049", 7, "Slow but beautiful."),
            ("The Godfather", 10, "A classic."),
        ]

        for title, score, comment in ratings:
            movie = Movie.objects.get(title=title)
            Rating.objects.get_or_create(
                movie=movie,
                score=score,
                defaults={"comment": comment},
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Genres: {Genre.objects.count()} | Movies: {Movie.objects.count()} "
                f"| People: {Person.objects.count()} | Ratings: {Rating.objects.count()}"
            )
        )
