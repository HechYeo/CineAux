from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This will save the user with a hashed password
            messages.success(request, "Registration successful. You can now log in.")
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


def dashboard(request):
    return render(request, "users/dashboard.html")



def logout_view(request):
    logout(request)  # This will log the user out
    return redirect('login')  # Redirect to the login page after logout
