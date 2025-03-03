from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_showtimes, name='movie_showtimes'),
    path('profile/', views.profile, name='profile'),  # Add this line
    path('add_movie/', views.add_movie, name='add_movie'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)