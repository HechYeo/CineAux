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
the_dark_knight = Movie.objects.get(title="The Dark Knight")
interstellar = Movie.objects.get(title="Interstellar")
parasite = Movie.objects.get(title="Parasite")
the_lion_king = Movie.objects.get(title="The Lion King")
spider_man_spider_verse = Movie.objects.get(title="Spider-Man: Into the Spider-Verse")
avengers_endgame = Movie.objects.get(title="Avengers: Endgame")
avengers_infinity_war = Movie.objects.get(title="Avengers: Infinity War")


# Get all showtimes for these movies
psycho_pass_showtimes = Showtime.objects.filter(movie=psycho_pass)
your_name_showtimes = Showtime.objects.filter(movie=your_name)
solo_leveling_showtimes = Showtime.objects.filter(movie=solo_leveling)
the_dark_knight_showtimes = Showtime.objects.filter(movie=the_dark_knight)
interstellar_showtimes = Showtime.objects.filter(movie=interstellar)
parasite_showtimes = Showtime.objects.filter(movie=parasite)
the_lion_king_showtimes = Showtime.objects.filter(movie=the_lion_king)
spider_man_spider_verse_showtimes = Showtime.objects.filter(movie=spider_man_spider_verse)
avengers_endgame_showtimes = Showtime.objects.filter(movie=avengers_endgame)
avengers_infinity_war_showtimes = Showtime.objects.filter(movie=avengers_infinity_war)



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
create_seats_for_showtimes(the_dark_knight_showtimes)
create_seats_for_showtimes(interstellar_showtimes)
create_seats_for_showtimes(parasite_showtimes)
create_seats_for_showtimes(the_lion_king_showtimes)
create_seats_for_showtimes(spider_man_spider_verse_showtimes)
create_seats_for_showtimes(avengers_endgame_showtimes)
create_seats_for_showtimes(avengers_infinity_war_showtimes)