from core.forms import CommentForm
from core.models import Comment, Movie
from django.shortcuts import HttpResponse,render, redirect, get_object_or_404

def add_commentary(request,slug):
    movie = get_object_or_404(Movie, slug=slug)
    form = CommentForm()
    if request.method == 'POST': 
        form = CommentForm(request.POST)
        if form.is_valid:
            return HttpResponse("HOLA INMUNDO")
    return render("movie/<slug:slug>",{form:form})
