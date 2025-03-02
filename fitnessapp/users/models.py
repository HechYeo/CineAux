from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    fitness_goal = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.CharField(max_length=100, null=True)
    date = models.DateField(default=date.today)
    duration = models.IntegerField(default=0)
    sets = models.IntegerField(default=0)
    reps = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.exercise} on {self.date}' or 'No Exercise'