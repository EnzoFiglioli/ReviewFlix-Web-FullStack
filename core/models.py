from django.db import models
from django.utils.text import slugify

class Movie(models.Model):
    title = models.CharField(max_length=105)
    director = models.CharField(max_length=100)
    poster = models.CharField(max_length=254)
    year = models.IntegerField()
    genre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, default="", null=False)

    def average_rating(self):
        ratings = Rating.objects.filter(movie=self)
        if ratings.exists():
            return sum(rating.score for rating in ratings) / ratings.count()
        return 0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Movie, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} ({self.year})"

class User(models.Model):
    username = models.CharField(max_length=100) 
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return f"@{self.username}"

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    
    def __str__(self):
        return f"Usuario: {self.user.username} - Pelicula: {self.movie.title}"

    class Meta:
        unique_together = ("user", "movie")

class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commentary = models.TextField()
    
    def __str__(self):
        return f"{self.user} - {self.commentary[:20]}..."

    class Meta:
        unique_together = ("user", "movie")
