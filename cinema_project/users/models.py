from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator



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
        return f"{self.user.first_name} {self.user.last_name} - Profile"

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField()  # Duration in minutes
    poster = models.ImageField(upload_to='movie_poster/', blank=True, null=True)
    age_rating = models.CharField(max_length=10)
    youtube_trailer = models.URLField(blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)

    def __str__(self):
        return self.title

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    time = models.TimeField(null=True)  # Store time as a time object

    @property
    def available_seats(self):
        return Seat.objects.filter(showtime=self, is_taken=False).count()

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
    seats_numbers = models.TextField(default="")
    booked_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the booking was made

    def __str__(self):
        return f"{self.user.email} - {self.showtime.movie.title} at {self.showtime.time}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])  # 1 to 5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.movie.title} ({self.rating}/5)"

