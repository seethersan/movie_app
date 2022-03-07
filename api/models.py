from django.db import models
from django.core import serializers
from django.template.defaultfilters import slugify
from api.utils import intToRoman

def convert_person_to_dict(person):
    return {
        'first_name': person.first_name,
        'last_name': person.last_name
    }

def convert_movie_to_dict(movie):
    return {
        'title': movie.title,
        'release_year': int(movie.release_year),
        'slug': movie.slug
    }

class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    
    @property
    def movies_as_actor(self):
        movies = self.movie_set.filter(movie_person__role='A').all()
        actored_movies = [convert_movie_to_dict(movie) for movie in movies]
        return actored_movies

    @property
    def movies_as_director(self):
        movies = self.movie_set.filter(movie_person__role='D').all()
        directed_movies = [convert_movie_to_dict(movie) for movie in movies]
        return directed_movies

    @property
    def movies_as_producer(self):
        movies = self.movie_set.filter(movie_person__role='P').all()
        produced_movies = [convert_movie_to_dict(movie) for movie in movies]
        return produced_movies

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
        persons = self.members.filter(movie_person__role='A').all()
        casting = [convert_person_to_dict(person) for person in persons]
        return casting

    @property
    def directors(self):
        persons = self.members.filter(movie_person__role='D').all()
        directors = [convert_person_to_dict(person) for person in persons]
        return directors

    @property
    def producers(self):
        persons = self.members.filter(movie_person__role='P').all()
        producers = [convert_person_to_dict(person) for person in persons]
        return producers

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
