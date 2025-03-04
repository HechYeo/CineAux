from django.contrib import admin
from .models import Movie, Showtime 
# Register your models here.
# Register your model with Django Admin
admin.site.register(Movie)
admin.site.register(Showtime)