from django.contrib import admin
from .models import User, Movie, Comment, Rating

admin.site.register(User)
admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(Rating)