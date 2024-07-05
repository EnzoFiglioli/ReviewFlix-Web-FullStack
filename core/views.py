from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.http import request, HttpRequest
from .models import Movie, User, Rating, Comment
from .forms import MovieForm, LoginForm,RatingForm,CommentForm
from django.contrib import messages

def home(request):
    # try:
        # latest_movies = Movie.objects.all().order_by('-title')[:5]
        # if not latest_movies:
            # raise Movie.DoesNotExist
    # except Movie.DoesNotExist:
        # return HttpResponse({"message": "Error al recibir las ultimas 5 pelis"}, status=404)
    
    # context = {"last_movies": latest_movies}
    perfil = request.session.get("user",None)
    if perfil:
        context = {"perfil":perfil}
        return render(request, 'home.html',context)
    else:
        return render(request, 'home.html')

def search(request):
    usuarios = request.session.get("user",None)
    query = request.GET.get("title")
    # if request.metho
    return render(request, 'search.html',{"perfil":usuarios})

def movies(request):
    movies = Movie.objects.all()
    perfil = request.session.get("user",None)
    context = {'movies': movies,"perfil":perfil}
    return render(request, 'movies.html', context)

def contacto(request):
    return render(request, 'contact.html')

# Editar pelicula
def get_movie_edit(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies')
    else:
        form = MovieForm(instance=movie)
    context = {'form': form, 'movie': movie}
    return render(request, 'movie-edit.html', context)

# Detalles de la pelicula
def movie_detail(request, slug):
    perfil = request.session.get("user", None)
    movie = get_object_or_404(Movie, slug=slug)
    comentarios = Comment.objects.filter(movie=movie)
    form = RatingForm(request.POST or None)
    if request.method == "POST" and perfil:
        if form.is_valid():
            rating = form.save(commit=False)
            rating.movie = movie
            
            # Obtener la instancia del usuario a partir del diccionario de la sesión
            user_instance = User.objects.get(id=perfil['id'])
            rating.user = user_instance
            
            rating.save()
            messages.success(request, "Your rating has been submitted successfully!")
            return redirect("/movie/<slug:slug>/")
        else:
            messages.error(request, "There was an error with your rating. Please try again.")
    
    context = {
        "perfil": perfil,
        "movie": movie,
        "form": form,
        "comentarios":comentarios
    }
    
    return render(request, 'movie_detail.html', context)

# Agregar una nueva pelicula
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = MovieForm()
    perfil = request.session.get("user",None)
    context = {"perfil":perfil,"form":form}
    return render(request,'add-movie.html',context)

# Eliminar una pelicula
def delete_movie(request):
    movie = get_object_or_404(Movie)
    new_movie = HttpRequest.body
    if(request.method == 'POST'):
        if new_movie != None:    
            return  redirect("/")

# Iniciar Sesion
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            print ({"email":email,"password":password})
            usuarios = User.objects.all().values()
            for user in usuarios:
                if user["email"] == email and user["password"] == password:
                    request.session["user"] = user
                    return redirect("/")
        else:
            return redirect("/")
    else:
        form = LoginForm()
        return render(request,'login.html',{"form":form})

def usuarios(request):
    users = User.objects.all().values()
    if(users):
        return HttpResponse(users)

def mi_perfil(request):
    perfil = request.session.get("user",None)
    if perfil:
        context = {"perfil":perfil}
        return render(request,"profile.html",context)

def logout(request):
    request.session.flush()
    return redirect("/")

# Puntajes
def rate_movie(request, movie_id):
    # Obtener usuario autenticado
    if request.user.is_authenticated:
        user = request.user
    else:
        # Obtener usuario de la sesión si no está autenticado
        usuarioLog = request.session.get("user", None)
        if usuarioLog and "username" in usuarioLog:
            username = usuarioLog["username"]
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Manejar el caso en que el usuario no existe
                return redirect('login')  # Redirigir a la página de login o manejar según tu lógica
        else:
            # Manejar el caso en que no se pueda determinar el usuario
            return redirect('login')  # Redirigir a la página de login o manejar según tu lógica

    # Obtener la película
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            # Actualizar o crear la calificación
            rating, created = Rating.objects.update_or_create(
                user=user,
                movie=movie,
                defaults={'score': form.cleaned_data['score']}
            )
            # Redirigir a la página de detalles de la película
            return redirect('movie_detail', slug=movie.slug)
    else:
        form = RatingForm()

    context = {'form': form, 'movie': movie}
    return render(request, "rate_movie.html", context)

def all_movies(request):
    movies = Movie.objects.all().values()
    return HttpResponse(movies)

def add_commentary(request, slug):
    usuario = request.session.get("user", None)
    movie = get_object_or_404(Movie, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Guarda el comentario asociándolo con la película y el usuario actual
            comment = form.save(commit=False)
            comment.movie = movie
            # Obtiene el usuario de la sesión actual
            user_instance = User.objects.get(id=usuario['id'])  # Asegúrate de que 'id' exista en tu sesión
            comment.user = user_instance
            comment.save()
            return redirect('detail', slug=movie.slug)
        else:
            return HttpResponse("El formulario no es válido")
    else:
        form = CommentForm()
    
    context = {
        "form": form,
        "movie": movie,
        "perfil": usuario
    }
    return render(request, "movie_detail.html", context)