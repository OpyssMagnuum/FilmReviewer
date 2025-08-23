"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from filmr.views import DirectorViewSet, ActorViewSet, GenreViewSet, FilmViewSet, manage_genres, manage_actors, \
    manage_directors, add_film, movie_review, movie_list

r = DefaultRouter()
r.register('directors', DirectorViewSet)
r.register('actors', ActorViewSet)
r.register('genres', GenreViewSet)
r.register('films', FilmViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('genres/', manage_genres, name='manage_genres'),
    path('genres/add/', manage_genres, name='add_genre'),

    path('actors/', manage_actors, name='manage_actors'),
    path('actors/add/', manage_actors, name='add_actor'),

    path('directors/', manage_directors, name='manage_directors'),
    path('directors/add/', manage_directors, name='add_director'),  # в html файле name задействуется

    path('add_movie/', add_film, name='add_film'),
    path('add_movie/add/', add_film, name='add_film'),

    path('movie/<int:film_id>/review/', movie_review, name='movie_review'),

    path('movies/', movie_list, name='movie_list'),
] + r.urls
