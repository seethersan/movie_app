from rest_framework import serializers
from api.models import Alias, Person, Movie, Role

class AliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alias
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    movies_as_actor = serializers.ReadOnlyField()
    movies_as_director = serializers.ReadOnlyField()
    movies_as_producer = serializers.ReadOnlyField()

    aliases = AliasSerializer(read_only=True)

    class Meta:
        model = Person
        fields = "__all__"

class MovieSerializer(serializers.ModelSerializer):
    casting = serializers.ReadOnlyField()
    directors = serializers.ReadOnlyField()
    producers = serializers.ReadOnlyField()
    release_year_roman = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = "__all__"

