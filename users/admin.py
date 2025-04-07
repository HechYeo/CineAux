from django.contrib import admin
from .models import Movie, Showtime, User, Booking, Seat, Review, Genre

# Admin Models
admin.site.register(Movie)
admin.site.register(Showtime)
admin.site.register(User)
admin.site.register(Booking)
admin.site.register(Seat)
admin.site.register(Review)
admin.site.register(Genre)