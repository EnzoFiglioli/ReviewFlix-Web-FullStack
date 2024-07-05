from django.urls import path
from .views import home, search, contacto, movies, get_movie_edit, movie_detail, login, add_movie, delete_movie, usuarios, mi_perfil, logout, all_movies, rate_movie
from .views import add_commentary
urlpatterns = [
    path('', home, name="home"),
    path('search/', search, name="search"),
    path('contacto/', contacto, name="contacto"),
    path('movies/', movies, name="movies"),
    path('movie/edit/<slug:slug>/', get_movie_edit, name="edit_movie"),
    path('movie/<slug:slug>/',movie_detail, name="detail"),
    path('movie/<slug:slug>/add-commentary/', add_commentary, name="detail-commentary"),
    path('login/', login, name="login"),
    path('movie/add', add_movie, name="add_movie"),
    path('movie/delete/', delete_movie, name="delete_movie"),
    path('users/all', usuarios, name="usuarios"),
    path("profile/", mi_perfil, name="profile"),
    path("logout/",logout,name="logout"),
    path("allmovies/", all_movies, name="all_movies"),
    path('movie/<int:movie_id>/rate/', rate_movie, name='rate_movie')
]
