from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomPasswordChangeView

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_showtimes, name='movie_showtimes'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('movie/<int:movie_id>/showtime/<int:showtime_id>/choose_seat/', views.choose_seat, name='choose_seat'),
    path('book_seats/', views.book_seats, name='book_seats'),
    path('booking_confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('booked_seats/', views.booked_seats, name='booked_seats'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)