from django.db import models


# Create your models here.
class Director(models.Model):
    name = models.CharField(max_length=256)
    photo = models.ImageField()

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=256)
    photo = models.ImageField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=256)
    year = models.IntegerField()
    director = models.ManyToManyField(Director, related_name="director_name", blank=True)
    actor = models.ManyToManyField(Actor, related_name="actor_name", blank=True)
    genre = models.ManyToManyField(Genre, related_name="genre_name")
    film_or_series = models.BooleanField(default=True)
    watched = models.BooleanField(default=False)
    score = models.IntegerField(null=True)
    review = models.TextField(null=True)

    def __str__(self):
        return f'{self.title}, {self.year}'




