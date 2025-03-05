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

@login_required
def book_seats(request):
    # Retrieve booking data from POST (or fallback to GET)
    movie_id = request.POST.get('movie') or request.GET.get('movie')
    showtime_id = request.POST.get('showtime') or request.GET.get('showtime')
    seats_param = request.POST.get('seats') or request.GET.get('seats')
    
    if not (movie_id and showtime_id and seats_param):
        return HttpResponse("Missing booking information.")
    
    movie = get_object_or_404(Movie, id=movie_id)
    showtime = get_object_or_404(Showtime, id=showtime_id)
    
    # Split the comma-separated seat numbers (e.g., "A3")
    selected_seat_numbers = seats_param.split(',')
    print("Selected seat numbers from URL:", selected_seat_numbers)
    
    # Try to fetch matching Seat objects for this showtime
    seats = Seat.objects.filter(showtime=showtime, number__in=selected_seat_numbers)
    
    if request.method == 'POST':
        booked_seats = []
        if seats.exists():
            for seat in seats:
                if not seat.is_taken:
                    seat.is_taken = True
                    seat.save()
                    booked_seats.append(seat)
                else:
                    return HttpResponse("One or more selected seats are already booked.")
        else:
            # Fallback: use the raw list if no Seat objects are found
            booked_seats = selected_seat_numbers
        
        # Mark the booking as complete in the session
        request.session['booking_complete'] = True
        
        print("Booked seats:", [s.number if hasattr(s, 'number') else s for s in booked_seats])
        return render(request, 'users/booking_confirmation.html', {
            'movie': movie,
            'showtime': showtime,
            'booked_seats': booked_seats,
        })
    
    # GET branch: pass additional raw data so the review page shows selected seats
    return render(request, 'users/book_seats.html', {
        'movie': movie,
        'showtime': showtime,
        'seats': seats,  # might be empty if no Seat objects exist
        'seats_param': seats_param,
        'selected_seat_numbers': selected_seat_numbers,
    })

def booking_confirmation(request):
    # Remove session flag once the confirmation page is visited
    if 'booking_complete' in request.session:
        del request.session['booking_complete']
    
    # Pass the necessary data to the confirmation page
    movie = request.session.get('movie')
    showtime = request.session.get('showtime')
    booked_seats = request.session.get('booked_seats', [])
    
    return render(request, 'users/booking_confirmation.html', {
        'movie': movie,
        'showtime': showtime,
        'booked_seats': booked_seats,
    })

