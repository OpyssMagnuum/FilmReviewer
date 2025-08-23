from django.contrib import admin
from filmr.models import Film, Director, Genre, Actor

# Register your models here.
admin.site.register(Film)
admin.site.register(Director)
admin.site.register(Genre)
admin.site.register(Actor)
