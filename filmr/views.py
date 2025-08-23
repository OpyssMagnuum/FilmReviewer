from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.viewsets import ModelViewSet

from project.serializers import DirectorSerializer, ActorSerializer, GenreSerializer, FilmSerializer
from filmr.models import Film, Director, Genre, Actor


# Create your views here.
class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class FilmViewSet(ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


def manage_genres(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Genre.objects.create(name=name)
        return redirect('manage_genres')

    genres_list = Genre.objects.all().order_by('name')
    paginator = Paginator(genres_list, 7)  # Показывать 10 жанров на странице

    page_number = request.GET.get('page')
    genres = paginator.get_page(page_number)

    return render(request, 'general/genre_add.html', {'genres': genres})


def manage_actors(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        photo = request.FILES.get('photo')
        if name and photo:
            Actor.objects.create(name=name, photo=photo)
        return redirect('manage_actors')

    actors_list = Actor.objects.all().order_by('name')
    paginator = Paginator(actors_list, 7)  # Показывать 7 актёров на странице

    page_number = request.GET.get('page')
    actors = paginator.get_page(page_number)

    return render(request, 'general/actor_add.html', {'actors': actors})


def manage_directors(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        photo = request.FILES.get('photo')
        if name and photo:
            Director.objects.create(name=name, photo=photo)
        return redirect('manage_directors')

    directors_list = Director.objects.all().order_by('name')
    paginator = Paginator(directors_list, 7)  # Показывать 7 актёров на странице

    page_number = request.GET.get('page')
    directors = paginator.get_page(page_number)

    return render(request, 'general/director_add.html', {'directors': directors})


def add_film(request):
    if request.method == 'POST':
        # Получаем данные из формы
        title = request.POST.get('title')
        year = request.POST.get('year')
        genres_ids = request.POST.getlist('genre')
        directors_ids = request.POST.getlist('director')
        actors_ids = request.POST.getlist('actor')
        film_or_series = 'film_or_series' in request.POST
        watched = 'watched' in request.POST
        score = request.POST.get('score')
        review = request.POST.get('review')

        # Валидация данных
        if not title or not year:
            messages.error(request, 'Title and Year are required fields')
            return redirect('add_film')

        try:
            # Создаем фильм
            film = Film.objects.create(
                title=title,
                year=int(year),
                film_or_series=film_or_series,
                watched=False
            )

            # Добавляем связи ManyToMany
            film.genre.set(Genre.objects.filter(id__in=genres_ids))
            film.director.set(Director.objects.filter(id__in=directors_ids))
            film.actor.set(Actor.objects.filter(id__in=actors_ids))

            messages.success(request, f'Film "{title}" added successfully!')
            return redirect('movie_list')

        except Exception as e:
            messages.error(request, f'Error adding film: {str(e)}')
            return redirect('add_film')

    else:
        # GET запрос - отображаем форму
        directors = Director.objects.all().order_by('name')
        actors = Actor.objects.all().order_by('name')
        genres = Genre.objects.all().order_by('name')

        context = {
            'directors': directors,
            'actors': actors,
            'genres': genres,
        }

        return render(request, 'movies/add_movie.html', context)


def movie_review(request, film_id):
    film = get_object_or_404(Film, pk=film_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'save':
            film.score = request.POST.get('score')
            film.review = request.POST.get('review')
            film.watched = True
            film.save()
            return redirect('movie_list')

    return render(request, 'movies/review_movie.html', {'film': film})


def movie_list(request):
    genres = Genre.objects.all().order_by("name")
    directors = Director.objects.all().order_by("name")
    actors = Actor.objects.all().order_by("name")
    films = Film.objects.all().order_by("title")

    filter_type = request.GET.get('filter', 'all')
    genre_id = request.GET.get('genre_id')
    director_id = request.GET.get('director_id')
    actor_id = request.GET.get('actor_id')

    # Применяем фильтры в зависимости от выбранного типа
    if filter_type == 'watched':
        films = films.filter(watched=True)
    elif filter_type == 'unwatched':
        films = films.filter(watched=False)
    elif filter_type == 'by_genre' and genre_id:
        films = films.filter(genre__id=genre_id)
    elif filter_type == 'by_director' and director_id:
        films = films.filter(director__id=director_id)
    elif filter_type == 'by_actor' and actor_id:
        films = films.filter(actor__id=actor_id)

    # Пагинация - 10 фильмов на страницу
    paginator = Paginator(films, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'genres': genres,
        'directors': directors,
        'actors': actors,
        'films': page_obj,
        'current_filter': filter_type,
        'selected_genre': int(genre_id) if genre_id else None,
        'selected_director': int(director_id) if director_id else None,
        'selected_actor': int(actor_id) if actor_id else None,
    }
    return render(request, "movies/movie_list.html", context)