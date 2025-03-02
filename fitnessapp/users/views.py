from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from datetime import date

from .forms import ProfileForm
from .models import Profile
from .forms import WorkoutForm
from .models import Workout


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after successful login
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    try:
        # Try to fetch the user's profile, or create one if it doesn't exist
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()  # Save the updated profile data
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = ProfileForm(instance=user_profile)  # Prepopulate the form with current user data

    return render(request, 'users/profile.html', {'form': form})


@login_required
def dashboard(request):
    # You can pass any user-specific data here, e.g., profile, recent activities, etc.
    user_profile = request.user.profile if hasattr(request.user, 'profile') else None
    return render(request, 'users/dashboard.html', {'user_profile': user_profile})


@login_required
def workout_history(request):
    workouts = Workout.objects.all()
    return render(request, 'users/workout_history.html', {'workouts': workouts})


@login_required
def log_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user  # Associate the workout with the logged-in user
            # Remove the line that sets the date manually
            workout.save()
            return redirect('workout_history')  # Redirect to the workout history page
    else:
        form = WorkoutForm()

    return render(request, 'users/log_workout.html', {'form': form})

@login_required
def delete_old_workouts(request):
    if request.method == 'POST':
        # Delete all workouts for the logged-in user
        Workout.objects.filter(user=request.user).delete()

        return redirect('workout_history')  # Redirect back to workout history page

    return redirect('workout_history')  # In case of a GET request, just redirect to history page