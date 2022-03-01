from django.test import TestCase
from api.models import Alias, Person, Movie, Role


class MovieModelTestCase(TestCase):
    def setUp(self):
        self.test_person = Person(first_name='Juan', last_name='Perez')
        self.test_person.save()

        self.test_movie = Movie(title='La muerte', release_year='1997')
        self.test_movie.save()

        self.test_role = Role(movie=self.test_movie, person=self.test_person, role='A')
        self.test_role.save()

    def test_person_properties(self):
        self.assertEquals(self.test_person.movies_as_actor, self.test_movie)

    def test_movies_properties(self):
        self.assertEquals(self.test_movie.actors, self.test_person)

    def tearDown(self):
        self.test_role.delete()
        self.test_movie.delete()
        self.test_person.delete()