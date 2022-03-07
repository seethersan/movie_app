from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Person, Movie, Role
from api.serializers import PersonSerializer, MovieSerializer, RoleSerializer


class PersonViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PersonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        person = Person.objects.get(id=pk)
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    def update(self, request, pk=None):
        person = Person.objects.get(id=pk)
        serializer = PersonSerializer(instance=person, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        person = Person.objects.get(id=pk)
        person.delete()
        return Response(satus=status.HTTP_204_NO_CONTENT)

class MovieViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        movie = Movie.objects.get(id=pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def update(self, request, pk=None):
        movie = Movie.objects.get(id=pk)
        serializer = MovieSerializer(instance=movie, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        movie = Movie.objects.get(id=pk)
        movie.delete()
        return Response(satus=status.HTTP_204_NO_CONTENT)

class RoleViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        role = Role.objects.get(id=pk)
        serializer = RoleSerializer(role)
        return Response(serializer.data)

    def update(self, request, pk=None):
        role = Role.objects.get(id=pk)
        serializer = RoleSerializer(instance=role, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        role = Role.objects.get(id=pk)
        role.delete()
        return Response(satus=status.HTTP_204_NO_CONTENT)