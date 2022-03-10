from django.contrib import admin
from api.models import Profile, Reward, ProfileReward, Person, Movie

admin.site.register(Profile)
admin.site.register(Reward)
admin.site.register(ProfileReward)
admin.site.register(Person)
admin.site.register(Movie)