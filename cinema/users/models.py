from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email



    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname} - Profile"
    
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField()  # Duration in minutes
    poster = models.ImageField(upload_to='movie_poster/', blank=True, null=True)
    age_rating = models.CharField(max_length=10)  # For FSK rating

    def __str__(self):
        return self.title

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    time = models.TimeField(null=True)  # Store time as a time object

    def __str__(self):
        return f"{self.movie.title} - {self.time}"

    class Meta:
        ordering = ['time']


class Seat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    number = models.CharField(max_length=5)
    is_taken = models.BooleanField(default=False)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default=1)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seats_numbers = models.TextField(default=1)
    booked_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the booking was made

    def __str__(self):
        return f"{self.user.email} - {self.showtime.movie.title} at {self.showtime.time}"


