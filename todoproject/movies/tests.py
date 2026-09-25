from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from .models import Genre, Movie, Rating


class RecommendationsViewTests(TestCase):
    """Tests for the public recommendations view."""

    @classmethod
    def setUpTestData(cls):
        cls.action = Genre.objects.create(name="Action")
        cls.comedy = Genre.objects.create(name="Comedy")

        cls.low = Movie.objects.create(title="Low Rated", year=2000)
        cls.low.genres.add(cls.action)
        Rating.objects.create(movie=cls.low, score=3)

        cls.high = Movie.objects.create(title="Top Rated", year=2010)
        cls.high.genres.add(cls.action)
        Rating.objects.create(movie=cls.high, score=9)

        cls.other = Movie.objects.create(title="Other Genre", year=2020)
        cls.other.genres.add(cls.comedy)

    def test_view_is_public(self):
        response = self.client.get(reverse("movies:recommendations"))
        self.assertEqual(response.status_code, 200)

    def test_movies_ordered_by_best_rating(self):
        response = self.client.get(
            reverse("movies:recommendations_by_genre", args=[self.action.pk])
        )
        movies = list(response.context["movies"])
        self.assertEqual(movies[0], self.high)
        self.assertEqual(movies[1], self.low)

    def test_only_same_genre_movies(self):
        response = self.client.get(
            reverse("movies:recommendations_by_genre", args=[self.action.pk])
        )
        titles = [movie.title for movie in response.context["movies"]]
        self.assertNotIn("Other Genre", titles)


class EditorPermissionTests(TestCase):
    """Tests for the 'editores' group permissions."""

    @classmethod
    def setUpTestData(cls):
        content_type = ContentType.objects.get_for_model(Movie)
        cls.group, _ = Group.objects.get_or_create(name="editores")
        cls.group.permissions.set(
            Permission.objects.filter(
                content_type=content_type,
                codename__in=["add_movie", "change_movie"],
            )
        )
        cls.editor = User.objects.create_user(username="editor_test", password="12345")
        cls.editor.groups.add(cls.group)

    def test_editor_can_add_and_change_movies(self):
        self.assertTrue(self.editor.has_perm("movies.add_movie"))
        self.assertTrue(self.editor.has_perm("movies.change_movie"))

    def test_editor_cannot_delete_movies(self):
        self.assertFalse(self.editor.has_perm("movies.delete_movie"))
