from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Person, Movie, Reward, Role
from django.contrib.auth.models import User

import json


class MovieModelTestCase(TestCase):
    def setUp(self):
        self.test_person = Person(first_name='Juan', last_name='Perez')
        self.test_person.save()

        self.test_movie = Movie(title='La muerte', release_year=1997)
        self.test_movie.save()

        self.test_role = Role(movie=self.test_movie, person=self.test_person, role='A')
        self.test_role.save()

    def test_person_properties(self):
        movie = self.test_person.movies_as_actor[0]
        self.assertEquals(movie['id'], self.test_movie.id)

    def test_movies_properties(self):
        person = self.test_movie.casting[0]
        self.assertEquals(person['id'], self.test_person.id)

    def tearDown(self):
        self.test_role.delete()
        self.test_movie.delete()
        self.test_person.delete()

class RewardViewTestCase(APITestCase):
    def setUp(self):
        self.username = 'usuario'
        self.password = 'password'
        self.email = 'usuario@mail.com'
        self.data = {
            'username': self.username,
            'password': self.password
        }

    def test_reward_create(self):
        user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.assertEquals(user.is_active, 1, 'Active User')

        response = self.client.post('/token/', self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK, response.content)
        token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))

        response = self.client.post('/api/rewards', data={'entity_type': 'P', 'amount': 1.5})
        reward = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEquals(reward['entity_type'], 'P')

class MovieViewTestCase(APITestCase):
    def setUp(self):
        self.test_person_1 = Person(first_name='Juan', last_name='Perez')
        self.test_person_1.save()

        self.test_person_2 = Person(first_name='Lucho', last_name='Diaz')
        self.test_person_2.save()

        self.test_movie = Movie(title='La muerte', release_year=1997)
        self.test_movie.save()

        self.test_role_casting_1 = Role(movie=self.test_movie, person=self.test_person_1, role='A')
        self.test_role_casting_1.save()        

        self.test_role_casting_2 = Role(movie=self.test_movie, person=self.test_person_2, role='A')
        self.test_role_casting_2.save()

        self.test_role_director = Role(movie=self.test_movie, person=self.test_person_1, role='D')
        self.test_role_director.save()

        self.test_reward_person = Reward(entity_type='P', amount=1.2)
        self.test_reward_person.save()

        self.test_reward_movie = Reward(entity_type='M', amount=2.5)
        self.test_reward_movie.save()

        self.username = 'usuario'
        self.password = 'password'
        self.email = 'usuario@mail.com'
        self.data = {
            'username': self.username,
            'password': self.password
        }

    def test_movies_get(self):
        response = self.client.get('/api/movies')
        movies = json.loads(response.content)
        self.assertEquals(self.test_movie.id, movies[0]['id'])

    def test_persons_get(self):
        response = self.client.get('/api/persons')
        persons = json.loads(response.content)
        self.assertEquals(self.test_person_1.id, persons[0]['id'])
        self.assertEquals(self.test_person_2.id, persons[1]['id'])

    def test_movie_and_person_create(self):
        user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.assertEquals(user.is_active, 1, 'Active User')

        response = self.client.post('/token/', self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK, response.content)
        token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))

        response = self.client.post('/api/persons', data={'first_name': 'Pepe', 'last_name': 'Jimenez'})
        person = json.loads(response.content)
        self.person_id = person['id']
        self.assertEquals(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEquals(person['created_by'], user.profile.id)

        response = self.client.post('/api/movies', data={'title': 'La musaraña', 'release_year': '1999'})
        movie = json.loads(response.content)
        self.movie_id = movie['id']
        self.assertEquals(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEquals(movie['created_by'], user.profile.id)

        response = self.client.get('/api/profile-rewards/{}/{}/{}'.format(user.profile.id, '2022-03-01', '2022-03-31'))
        profile_rewards = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEquals(len(profile_rewards), 2)

        response = self.client.post('/api/roles', data={'movie': self.movie_id, 'person': self.person_id, 'role': 'A'})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED, response.content)

    def tearDown(self):
        self.test_role_casting_1.delete()
        self.test_role_casting_2.delete()
        self.test_role_director.delete()
        self.test_movie.delete()
        self.test_person_1.delete()
        self.test_person_2.delete()
        self.test_reward_person.delete()
        self.test_reward_movie.delete()