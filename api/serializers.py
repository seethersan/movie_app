from rest_framework import serializers
from api.models import Alias, Person, Movie, Role, Reward, Profile, ProfileReward

class AliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alias
        fields = '__all__'

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ProfileRewardSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = ProfileReward
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    movies_as_actor = serializers.ListField(read_only=True)
    movies_as_director = serializers.ListField(read_only=True)
    movies_as_producer = serializers.ListField(read_only=True)

    aliases = AliasSerializer(read_only=True)

    class Meta:
        model = Person
        fields = "__all__"

class MovieSerializer(serializers.ModelSerializer):
    casting = serializers.ListField(read_only=True)
    directors = serializers.ListField(read_only=True)
    producers = serializers.ListField(read_only=True)
    release_year_roman = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = "__all__"