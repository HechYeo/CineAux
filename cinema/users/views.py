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
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This will save the user with a hashed password
            return redirect('login')
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Try to authenticate the user using the email and password
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            print(f"User {user.email} logged in successfully")  # Debug print
            return redirect('dashboard')  # Ensure 'dashboard' is correct
        else:
            messages.error(request, 'Invalid email or password')
            print(f"Login failed for {email}")  # Debug print
    return render(request, 'users/login.html')

@login_required
def dashboard(request):
    movies = Movie.objects.all()  # Get all movies
    return render(request, 'users/dashboard.html', {'movies': movies})



def logout_view(request):
    logout(request)
    response = redirect('login')  # Redirect to login page
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