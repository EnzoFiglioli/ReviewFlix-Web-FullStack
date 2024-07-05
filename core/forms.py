from django import forms
from .models import Movie, User, Rating, Comment

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'year', 'director', 'poster', 'genre','slug']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class SearchForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title"]

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commentary']

        