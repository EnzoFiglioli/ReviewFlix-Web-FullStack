from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.http import request, HttpRequest
from .models import Movie, User, Rating, Comment
from .forms import MovieForm, LoginForm,RatingForm,CommentForm, RegisterForm, SearchForm
from django.contrib import messages

def home(request):
    perfil = request.session.get("user",None)
    last_movies = Movie.objects.order_by('-created_at')[:5]
    if last_movies is not None or last_movies is not None:
        context = {"perfil":perfil, 'last_movies':last_movies}
        return render(request, 'home.html',context)
    else:
        return render(request, 'home.html')

def search(request):
    form = SearchForm(request.GET or None)
    usuarios = request.session.get("user", None)
    query = request.GET.get("title", "")

    # Filtrar películas basadas en el título
    movies = Movie.objects.filter(title__icontains=query) if query else Movie.objects.none()

    # Verificar si hay películas en el QuerySet y si el formulario es válido
    if form.is_valid() or movies.exists():
        context = {
            "usuarios": usuarios,
            "results": movies,  # Usar 'results' para los resultados en la plantilla
            "query": query,
            "form": form
        }
        return render(request, 'search.html', context)
    else:
        messages.error(request, "No se encontraron películas con ese nombre.")

    # Renderizar la página con el formulario si no se encontraron películas
    context = {
        'perfil': usuarios,
        'form': form
    }
    return render(request, 'search.html', context)


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
    rate_count = Rating.objects.filter(movie=movie).values('user').distinct().count()
    form = RatingForm(request.POST or None)
    
    if request.method == "POST" and perfil:
        if form.is_valid():
            rating = form.save(commit=False)
            rating.movie = movie
            user_instance = User.objects.get(id=perfil['id'])
            rating.user = user_instance
            
            if Rating.objects.filter(user=user_instance, movie=movie).exists():
                messages.error(request, "Ya has puntuado esta película.")
            else:
                rating.save()
                messages.success(request, "Tu puntuación ha sido enviada correctamente.")
            return redirect("detail", slug=slug)
        else:
            messages.error(request, "Hubo un error con tu puntuación. Por favor, inténtalo de nuevo.")
    
    context = {
        "perfil": perfil,
        "movie": movie,
        "form": form,
        "comentarios": comentarios,
        "rate_count": rate_count,
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

# Registro de usuario
def register(request):
    form = RegisterForm()
    context = {'form':form}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
        else:
            return render(request,'register.html',context)
    return render(request,'register.html',context)

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
            user_instance = User.objects.get(id=usuario['id'])
            # Verificar si el usuario ya ha dejado un comentario para esta película
            if Comment.objects.filter(user=user_instance, movie=movie).exists():
                messages.error(request, "Ya has dejado un comentario para esta película.")
            else:
                comment = form.save(commit=False)
                comment.movie = movie
                comment.user = user_instance
                comment.save()
                messages.success(request, "Tu comentario ha sido enviado correctamente.")
            return redirect('detail', slug=movie.slug)
        else:
            messages.error(request, "Hubo un error con tu comentario. Por favor, inténtalo de nuevo.")
    
    form = CommentForm()
    context = {
        "form": form,
        "movie": movie,
        "perfil": usuario,
    }
    
    return render(request, "movie_detail.html", context)
