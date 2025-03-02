from django import forms
from .models import Profile
from .models import Workout


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['weight', 'height', 'age', 'fitness_goal']


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['exercise', 'date', 'duration', 'sets', 'reps']
