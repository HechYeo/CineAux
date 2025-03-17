from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Movie, Showtime, Seat, Booking, User
from .forms import UserRegistrationForm, ReviewForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.http import Http404
from urllib.parse import urlparse, parse_qs
from django.core.paginator import Paginator

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


@login_required
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
    
    # Add JavaScript to reload the page
    response.content = response.content.replace(
        b'</body>', 
        b'<script type="text/javascript">window.location.reload();</script></body>'
    )
    
    return response

@login_required
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'users/movie_list.html', {'movies': movies})

@login_required
def movie_showtimes(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = Showtime.objects.filter(movie=movie)
    reviews = movie.reviews.all()
    max_rating = 5
    trailer_url = movie.youtube_trailer
    video_id = None

    # Extract video ID from YouTube URL
    if 'youtube.com' in trailer_url:
        parsed_url = urlparse(trailer_url)
        video_id = parse_qs(parsed_url.query).get('v', [None])[0]
        print(video_id)

    return render(request, 'users/movie_showtimes.html', {'movie': movie, 'showtimes': showtimes, 'reviews': reviews, 'video_id': video_id})


@login_required
def profile(request):
    # Get the currently logged-in user
    user = request.user
    return render(request, 'users/profile.html', {'user': user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save() 
            return redirect('profile') 
        else:
            messages.error(request, "There was an error updating your profile.") 
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('profile') 

    def form_valid(self, form):
        messages.success(self.request, "Password changed successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error changing your password.") 
        return super().form_invalid(form)

@login_required
def choose_seat(request, movie_id, showtime_id):
    # Get the showtime object from the database using the provided showtime_id
    showtime = get_object_or_404(Showtime, id=showtime_id)
    
    # Access the related movie object
    movie = showtime.movie
    
    # Get the seats for this showtime (assuming Seat model links to Showtimes)
    seats = Seat.objects.filter(showtime=showtime)
    
    # Get the bookings for the showtime
    booked_seats_queryset = showtime.booking_set.all()  # Query all bookings for this showtime
    
    # Initialize the booked_seats list as an empty list
    booked_seats = []

    # Populate the booked_seats list with the seat numbers from each booking
    for booking in booked_seats_queryset:
        # Assuming 'seats_numbers' is a comma-separated string
        booked_seats.extend(booking.seats_numbers.split(','))
    
    # Now, pass 'booked_seats' to the template along with the other context
    return render(request, 'users/choose_seat.html', {
        'showtime': showtime,
        'movie': movie,
        'seats': seats,
        'booked_seats': booked_seats  # Pass the list of booked seat numbers to the template
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
        missing_seats = []

        for seat_number in selected_seat_numbers:
            seat = seats.filter(number=seat_number).first()
            if seat:
                if not seat.is_taken:
                    seat.is_taken = True
                    seat.save()
                    booked_seats.append(seat)
                else:
                    already_taken.append(seat.number)
            else:
                missing_seats.append(seat_number)

        if already_taken:
            messages.error(request, f"Seats already booked: {', '.join(already_taken)}. Please select different seats.")
            return redirect(request.META.get('HTTP_REFERER', 'book_seats'))

        if missing_seats:
            messages.error(request, f"Some seats were not found: {', '.join(missing_seats)}. Please try again.")
            return redirect(request.META.get('HTTP_REFERER', 'book_seats'))

        # Save booking in the database
        booking = Booking.objects.create(
            user=request.user, 
            movie=movie, 
            showtime=showtime, 
            seats_numbers=','.join([seat.number for seat in booked_seats])
        )

        request.session['movie'] = movie.id
        request.session['showtime'] = showtime.id
        request.session['booked_seats'] = [seat.number for seat in booked_seats]  # Store seat numbers, not objects
        request.session['booking_complete'] = True

        print(f"Booking completed: {booking}")
        print(f"Booked seats: {request.session['booked_seats']}")
        print("✅ Booking complete session set!")  # Debugging print

        return redirect('booking_confirmation')


    return render(request, 'users/book_seats.html', {
        'movie': movie,
        'showtime': showtime,
        'seats': seats,
        'seats_param': seats_param,
        'selected_seat_numbers': selected_seat_numbers,
    })


@login_required
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
    
    return redirect('/dashboard')  # In case the session is not valid



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
        booking = get_object_or_404(Booking, id=booking_id)

        # Split seat numbers from the text field
        seats = booking.seats_numbers.split(',')

        # Ensure the seat number is valid
        if seat_number not in seats:
            messages.error(request, "Selected seat is not part of this booking.")
            return redirect('booked_seats')

        # Remove the seat from the list
        seats.remove(seat_number)
        booking.seats_numbers = ','.join(seats)
        booking.save()

        # Get the showtime for this booking
        showtime = booking.showtime

        # Get the seat object safely
        seat = get_object_or_404(Seat, showtime=showtime, number=seat_number)
        seat.is_taken = False
        seat.save()

        # If no more seats are booked, delete the booking
        if not booking.seats_numbers:
            booking.delete()

        # Success message for cancellation
        messages.success(request, f"Seat {seat_number} has been canceled successfully.")
        return redirect('booked_seats')

    except Booking.DoesNotExist:
        raise Http404("Booking not found")
    except Seat.DoesNotExist:
        raise Http404("Seat not found")

@login_required
def transfer_seat(request, booking_id, seat_number):
    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email')

        # Validate recipient
        try:
            recipient = User.objects.get(email=recipient_email)
        except User.DoesNotExist:
            messages.error(request, "No account found with that email address.")
            return redirect('booked_seats')  # Redirect to the booked seats page

        booking = get_object_or_404(Booking, id=booking_id)

        # Ensure the seat exists in this booking
        seats = booking.seats_numbers.split(',')
        if seat_number not in seats:
            messages.error(request, "Selected seat is not part of this booking.")
            return redirect('booked_seats')

        # Remove the seat from the original booking
        seats.remove(seat_number)
        if seats:
            booking.seats_numbers = ','.join(seats)
            booking.save()
        else:
            # If no more seats remain, delete the booking
            booking.delete()

        # Create or update a new booking for the recipient
        new_booking, created = Booking.objects.get_or_create(
            user=recipient, movie=booking.movie, showtime=booking.showtime
        )

        # Append the transferred seat to the recipient's booking
        if new_booking.seats_numbers:
            new_seats = new_booking.seats_numbers.split(',')
            new_seats.append(seat_number)
            new_booking.seats_numbers = ','.join(new_seats)
        else:
            new_booking.seats_numbers = seat_number
        new_booking.save()

        # Mark the seat as taken by the new owner
        seat = get_object_or_404(Seat, showtime=booking.showtime, number=seat_number)
        seat.is_taken = True
        seat.save()

        # Success message (optional)
        messages.success(request, f"Seat {seat_number} has been successfully transferred to {recipient_email}.")
        return redirect('booked_seats')

    return redirect('booked_seats')


@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('movie_showtimes', movie_id=movie.id)
    else:
        # Initialize an empty form for GET request
        form = ReviewForm()

    return render(request, 'users/add_review.html', {'form': form, 'movie': movie})

@login_required
def all_movies(request):
    movies = Movie.objects.all()

    # Check if the user has selected a sort option
    sort_order = request.GET.get('sort', None)

    # Sort movies if a sort option is selected
    if sort_order == '-title':
        movies = movies.order_by('-title')
    elif sort_order == 'title':
        movies = movies.order_by('title')

    return render(request, 'users/all_movies.html', {'movies': movies})

@login_required
def movie_reviews(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews_list = movie.reviews.all().order_by('-created_at')  # Latest reviews first
    paginator = Paginator(reviews_list, 8)  # Show 8 reviews per page

    page_number = request.GET.get('page')  # Get the page number from the URL
    page_reviews = paginator.get_page(page_number)

    return render(request, 'users/movie_reviews.html', {
        'movie': movie,
        'reviews': page_reviews
    })