from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Movie, Showtime
from .forms import MovieForm
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import Movie, Showtime, Seat
from django.http import HttpResponse

def register(request):
    # If the user is already logged in, don't show the register page
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This will save the user with a hashed password
            return redirect('login')  # Redirect to login after successful registration
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    # If the user is already logged in, don't show the login page
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect to dashboard if already logged in

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)  # Log in the user
            return redirect('dashboard')  # Redirect after successful login
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'users/login.html')



def dashboard(request):
    movies = Movie.objects.all()  # Get all movies
    return render(request, 'users/dashboard.html', {'movies': movies})


@login_required
def logout_view(request):
    logout(request)  # Log out the user
    response = redirect('login')  # Redirect to login page
    # Apply no-cache headers after logout to avoid back-button issue
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'users/movie_list.html', {'movies': movies})

def movie_showtimes(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = Showtime.objects.filter(movie=movie)
    return render(request, 'users/movie_showtimes.html', {'movie': movie, 'showtimes': showtimes})

@login_required
def profile(request):
    # Get the currently logged-in user
    user = request.user
    return render(request, 'users/profile.html', {'user': user})

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)  # Handle file upload
        if form.is_valid():
            form.save()
            return redirect('users/dashboard')  # Redirect to dashboard or movie list
    else:
        form = MovieForm()
    
    return render(request, 'users/add_movie.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect back to the profile page
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/change_password.html'  # Path to your template
    success_url = reverse_lazy('profile')  # Redirect to the profile page after successful password change

def choose_seat(request, movie_id, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    movie = showtime.movie  # Access the movie related to this showtime
    return render(request, 'users/choose_seat.html', {
        'showtime': showtime,
        'movie': movie  # Pass the movie object to the template
    })