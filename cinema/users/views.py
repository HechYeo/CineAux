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
from .models import Movie, Showtime, Seat, Booking
from django.http import HttpResponse
from django.http import Http404
from django.db import transaction

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
    movie_id = request.POST.get('movie') or request.GET.get('movie')
    showtime_id = request.POST.get('showtime') or request.GET.get('showtime')
    seats_param = request.POST.get('seats') or request.GET.get('seats')
    
    if not (movie_id and showtime_id and seats_param):
        return HttpResponse("Missing booking information.")
    
    movie = get_object_or_404(Movie, id=movie_id)
    showtime = get_object_or_404(Showtime, id=showtime_id)
    
    selected_seat_numbers = seats_param.split(',')
    print("Selected seat numbers from URL:", selected_seat_numbers)
    
    seats = Seat.objects.filter(showtime=showtime, number__in=selected_seat_numbers)
    
    if request.method == 'POST':
        booked_seats = []
        already_taken = []
        if seats.exists():
            for seat in seats:
                if not seat.is_taken:
                    seat.is_taken = True
                    seat.save()
                    booked_seats.append(seat)
                else:
                    already_taken.append(seat.number)
            if already_taken:
                # Add error message instead of returning HttpResponse
                messages.error(request, "One or more selected seats are already booked: " + ", ".join(already_taken))
                return redirect('book_seats')
        else:
            booked_seats = selected_seat_numbers
        
        # Save booking in the database
        booking = Booking.objects.create(
            user=request.user, 
            movie=movie, 
            showtime=showtime, 
            seats_numbers=','.join(selected_seat_numbers)
        )
        
        request.session['movie'] = movie.id
        request.session['showtime'] = showtime.id
        request.session['booked_seats'] = [seat.number for seat in booked_seats]
        request.session['booking_complete'] = True
        
        print(f"Booking completed: {booking}")
        print(f"Booked seats: {[seat.number for seat in booked_seats]}")
        
        return redirect('booking_confirmation')
    
    return render(request, 'users/book_seats.html', {
        'movie': movie,
        'showtime': showtime,
        'seats': seats,
        'seats_param': seats_param,
        'selected_seat_numbers': selected_seat_numbers,
    })


def booking_confirmation(request):
    if 'booking_complete' in request.session:
        # Remove session flag after confirmation page is visited
        del request.session['booking_complete']
        # Continue with rendering confirmation page
        movie_id = request.session.get('movie')
        showtime_id = request.session.get('showtime')
        booked_seats = request.session.get('booked_seats', [])
        
        movie = get_object_or_404(Movie, id=movie_id)
        showtime = get_object_or_404(Showtime, id=showtime_id)
        
        return render(request, 'users/booking_confirmation.html', {
            'movie': movie,
            'showtime': showtime,
            'booked_seats': booked_seats,
        })
    
    return redirect('users:dashboard')  # In case the session is not valid



@login_required
def booked_seats(request):
    # Get the bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user)

    # Preprocess the seats_numbers to split it into a list
    for booking in bookings:
        booking.seats_list = booking.seats_numbers.split(',')

    return render(request, 'users/booked_seats.html', {
        'bookings': bookings
    })

@login_required
def cancel_booking(request, booking_id, seat_number):
    try:
        # Get the booking based on booking_id
        booking = Booking.objects.get(id=booking_id)
        
        # Split seat numbers from the text field
        seats = booking.seats_numbers.split(',')

        # If seat is in the list of booked seats, remove it
        if seat_number in seats:
            seats.remove(seat_number)
            booking.seats_numbers = ','.join(seats)
            booking.save()
            
            # Get the showtime for this booking
            showtime = booking.showtime
            
            # Mark the seat as available
            seat = Seat.objects.get(showtime=showtime, number=seat_number)
            seat.is_taken = False
            seat.save()
        
        # If no more seats are booked, delete the entire booking
        if not booking.seats_numbers:
            booking.delete()
        
        # Redirect to the booked seats page
        return redirect('booked_seats')
    
    except Booking.DoesNotExist:
        raise Http404("Booking not found")
    except Seat.DoesNotExist:
        raise Http404("Seat not found")
