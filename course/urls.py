from django.urls import path
from . import views

urlpatterns = [
    path("", views.search, name = "search"),
    path("courses/<str:subject_number>", views.course, name = "course")
    #path("/search?subject_number=<str:subject_number>", views.course, name = "course")
]
