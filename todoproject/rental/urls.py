from django.urls import path

from . import views

app_name = "rental"

urlpatterns = [
    path("", views.equipo_list, name="equipo_list"),
    path("nuevo/", views.equipo_create, name="equipo_create"),
]