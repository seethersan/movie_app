from django.test import TestCase
from rest_framework.test import APITestCase
from api.models import Person, Movie, Role, convert_movie_to_dict, convert_person_to_dict

import json


class MovieModelTestCase(TestCase):
    def setUp(self):
        self.test_person = Person(first_name='Juan', last_name='Perez')
        self.test_person.save()

        self.test_movie = Movie(title='La muerte', release_year='1997')
        self.test_movie.save()

        self.test_role = Role(movie=self.test_movie, person=self.test_person, role='A')
        self.test_role.save()

    def test_person_properties(self):
        self.assertEquals(self.test_person.movies_as_actor[0], convert_movie_to_dict(self.test_movie))

    def test_movies_properties(self):
        self.assertEquals(self.test_movie.casting[0], convert_person_to_dict(self.test_person))

    def tearDown(self):
        self.test_role.delete()
        self.test_movie.delete()
        self.test_person.delete()

class MovieViewTestCase(APITestCase):
    def setUp(self):
        self.test_person_1 = Person(first_name='Juan', last_name='Perez')
        self.test_person_1.save()

        self.test_person_2 = Person(first_name='Lucho', last_name='Diaz')
        self.test_person_2.save()

        self.test_movie = Movie(title='La muerte', release_year='1997')
        self.test_movie.save()

        self.test_role_casting_1 = Role(movie=self.test_movie, person=self.test_person_1, role='A')
        self.test_role_casting_1.save()        

        self.test_role_casting_2 = Role(movie=self.test_movie, person=self.test_person_2, role='A')
        self.test_role_casting_2.save()

        self.test_role_director = Role(movie=self.test_movie, person=self.test_person_1, role='D')
        self.test_role_director.save()

    def test_movies_get(self):
        response = self.client.get('/api/movies')
        movies = json.loads(response.content)
        self.assertDictContainsSubset(convert_movie_to_dict(self.test_movie), movies[0])

    def test_persons_get(self):
        response = self.client.get('/api/persons')
        persons = json.loads(response.content)
        self.assertDictContainsSubset(convert_person_to_dict(self.test_person_1), persons[0])
        self.assertDictContainsSubset(convert_person_to_dict(self.test_person_2), persons[1])

    def tearDown(self):
        self.test_role_casting_1.delete()
        self.test_role_casting_2.delete()
        self.test_role_director.delete()
        self.test_movie.delete()
        self.test_person_1.delete()
        self.test_person_2.delete()