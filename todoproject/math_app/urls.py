from django.urls import path
from . import views

urlpatterns = [
    path('', views.math_operations, name='math_operations'),
]