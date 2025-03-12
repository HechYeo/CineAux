from users.models import Movie, Showtime, Seat

# Define seat rows and numbers
seat_structure = {
    "A": range(1, 4),
    "B": range(1, 9),
    "C": range(1, 12),
    "D": range(1, 18),
    "E": range(1, 18),
    "F": range(1, 18),
    "G": range(1, 18),
    "H": range(1, 16),
    "I": range(1, 16),
    "J": range(1, 16),
    "K": range(1, 16),
    "L": range(1, 19),
    "M": range(1, 15),
}

# Get the movies
psycho_pass = Movie.objects.get(title="Psycho-Pass - The Movie")
your_name = Movie.objects.get(title="Your Name")
solo_leveling = Movie.objects.get(title="Solo Leveling: ReAwakening")

# Get all showtimes for these movies
psycho_pass_showtimes = Showtime.objects.filter(movie=psycho_pass)
your_name_showtimes = Showtime.objects.filter(movie=your_name)
solo_leveling_showtimes = Showtime.objects.filter(movie=solo_leveling)

def create_seats_for_showtimes(showtimes):
    seats = []
    for showtime in showtimes:
        for row, numbers in seat_structure.items():
            for num in numbers:
                seat_number = f"{row}{num}"
                seat = Seat(showtime=showtime, number=seat_number, is_taken=False)
                seats.append(seat)
    Seat.objects.bulk_create(seats)  # Bulk create for efficiency
    print(f"Created {len(seats)} seats.")

# Create seats for both movies
create_seats_for_showtimes(psycho_pass_showtimes)
create_seats_for_showtimes(your_name_showtimes)
create_seats_for_showtimes(solo_leveling_showtimes)