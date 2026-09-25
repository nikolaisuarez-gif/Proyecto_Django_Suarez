from django.urls import path

from . import views

app_name = "movies"

urlpatterns = [
    path("recommendations/", views.recommendations, name="recommendations"),
    path("recommendations/<int:genre_id>/", views.recommendations, name="recommendations_by_genre"),
]
