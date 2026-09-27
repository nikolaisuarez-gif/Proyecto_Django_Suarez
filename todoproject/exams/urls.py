from django.urls import path

from . import views

app_name = "exams"

urlpatterns = [
    path("", views.exam_list, name="exam_list"),
    path("nuevo/", views.exam_create, name="exam_create"),
    path("<int:pk>/", views.exam_detail, name="exam_detail"),
    path("<int:pk>/pregunta/nueva/", views.question_add, name="question_add"),
    path("pregunta/<int:pk>/", views.question_detail, name="question_detail"),
]
