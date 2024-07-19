from django import forms
from .models import Movie, User, Rating, Comment

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'year', 'director', 'poster', 'genre','description']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User        
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder':'ejemplo@reviewflix.com'}),
            'password': forms.PasswordInput(attrs={'placeholder':'Tu password va aquí'})
            }
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','password','username']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder':'ejemplo@reviewflix.com'}),
            'password':forms.PasswordInput(attrs={'placeholder':'Tu password va aquí'}),
            'username':forms.TextInput(attrs={'placeholder':'Tu nombre de usuario'})
        }

class SearchForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title"]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Tu busqueda aquí'})
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={'min': 1, 'max': 5, 'placeholder':'Puntua con un numero entre 1 y 5'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commentary']
        widgets = {
            'commentary': forms.TextInput(attrs={'placeholder':'Que opinas de esta pelicula?'})
        }