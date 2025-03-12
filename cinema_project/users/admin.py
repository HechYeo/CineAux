from django.contrib import admin
from .models import Movie, Showtime, User, Booking, Seat
# Register your models here.
# Register your model with Django Admin
admin.site.register(Movie)
admin.site.register(Showtime)
admin.site.register(User)
admin.site.register(Booking)
admin.site.register(Seat)
