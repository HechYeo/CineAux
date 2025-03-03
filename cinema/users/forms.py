from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import User, Profile, Movie

User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField()  # Input field for email
    password = forms.CharField(widget=forms.PasswordInput)  # Input field for password


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']
        labels = {
            'first_name': 'Vorname',  # Change First Name to Vorname
            'last_name': 'Nachname',   # Change Last Name to Nachname
            'password': 'Password',    # Keep Password in English (can change if needed)
            'confirm_password': 'Passwort bestätigen',  # Change Confirm Password to Passwort bestätigen
            'email': 'E-Mail'          # Change Email to E-Mail
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age']

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'duration', 'poster']
