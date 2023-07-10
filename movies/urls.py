from django.urls import path
from .views import MovieListCreateView, MovieRetrieveUpdateDestroyView

app_name = "movies"

urlpatterns = [
    path("", MovieListCreateView.as_view(), name="movie-list-create"),
    path(
        "<int:pk>/",
        MovieRetrieveUpdateDestroyView.as_view(),
        name="movie-retrieve-update-destroy",
    ),
]
