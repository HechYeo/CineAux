from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import User, Movie, Review
from django.core.validators import RegexValidator

User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, validators=[RegexValidator(r'^[a-zA-Z\s]*$', 'Only alphabetic characters and spaces are allowed.')])
    last_name = forms.CharField(max_length=30, validators=[RegexValidator(r'^[a-zA-Z\s]*$', 'Only alphabetic characters and spaces are allowed.')])
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

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


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'duration', 'age_rating', 'poster', 'youtube_trailer']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(6)]  # Rating choices from 0 to 5

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select, required=True)
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']
