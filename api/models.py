from django.db import models
from django.template.defaultfilters import slugify
from api.utils import intToRoman

class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    
    @property
    def movies_as_actor(self):
        movies = self.movie_set.filter(movie_person__role='A').get()
        return movies

    @property
    def movies_as_director(self):
        movies = self.movie_set.filter(movie_person__role='D').get()
        return movies

    @property
    def movies_as_producer(self):
        movies = self.movie_set.filter(movie_person__role='P').get()
        return movies

class Alias(models.Model):
    name = models.CharField(max_length=200)
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
    )

class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.SmallIntegerField()
    slug = models.SlugField(blank=True)
    members = models.ManyToManyField(Person,
        through='Role',
        through_fields=('movie', 'person'))

    def save(self, **kwargs):
        self.slug = slugify(self.title) 
        super(Movie, self).save(**kwargs)

    @property
    def casting(self):
        persons = self.members.filter(movie_person__role='A').get()
        return persons

    @property
    def directors(self):
        persons = self.members.filter(movie_person__role='D').get()
        return persons

    @property
    def producers(self):
        persons = self.members.filter(movie_person__role='P').get()
        return persons

    @property
    def release_year_roman(self):
        return intToRoman(self.release_year)

class Role(models.Model):
    PERSON_MOVIE_ROLES = [
        ('A', 'Actor/Actress'),
        ('D', 'Director'),
        ('P', 'Producer')
    ]
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_person')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='movie_person')
    role = models.CharField(max_length=1, choices=PERSON_MOVIE_ROLES)
