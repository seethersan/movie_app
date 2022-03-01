from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    
    @property
    def movies_as_actor(self):
        movies = Movie.objects.filter(person__id=self.id).filter(members__role='A')
        return movies

    @property
    def movies_as_director(self):
        movies = Movie.objects.filter(person__id=self.id).filter(members__role='D')
        return movies

    @property
    def movies_as_producer(self):
        movies = Movie.objects.filter(person__id=self.id).filter(members__role='P')
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
    members = models.ManyToManyField(Person,
        through='Role',
        through_fields=('movie', 'person'))

    @property
    def actors(self):
        persons = Person.objects.filter(movie__id=self.id).filter(members__role='A')
        return persons

    @property
    def directors(self):
        persons = Person.objects.filter(movie__id=self.id).filter(members__role='D')
        return persons

    @property
    def producers(self):
        persons = Person.objects.filter(movie__id=self.id).filter(members__role='P')
        return persons

class Role(models.Model):
    PERSON_MOVIE_ROLES = [
        ('A', 'Actor/Actress'),
        ('D', 'Director'),
        ('P', 'Producer')
    ]
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=PERSON_MOVIE_ROLES)
