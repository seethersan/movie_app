from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from api.utils import intToRoman
from django.forms.models import model_to_dict

User = get_user_model()

ENTITY_TYPE = [
        ('M', 'Movie'),
        ('P', 'Person')
    ]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    earned_points = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.user.username

class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null= True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def movies_as_actor(self):
        movies = self.movie_set.filter(movie_person__role='A').values()
        return movies

    @property
    def movies_as_director(self):
        movies = self.movie_set.filter(movie_person__role='D').values()
        return movies

    @property
    def movies_as_producer(self):
        movies = self.movie_set.filter(movie_person__role='P').values()
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
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null= True)
    members = models.ManyToManyField(Person,
        through='Role',
        through_fields=('movie', 'person'))

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super(Movie, self).save(**kwargs)

    def __str__(self):
        return self.title

    @property
    def casting(self):
        persons = self.members.filter(movie_person__role='A').values()
        return persons

    @property
    def directors(self):
        persons = self.members.filter(movie_person__role='D').values()
        return persons

    @property
    def producers(self):
        persons = self.members.filter(movie_person__role='P').values()
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

class Reward(models.Model):
    entity_type = models.CharField(max_length=1, choices=ENTITY_TYPE, primary_key=True)
    amount = models.FloatField()

    def __str__(self):
        return self.entity_type

class ProfileReward(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_reward')
    entity_type = models.CharField(max_length=1, choices=ENTITY_TYPE)
    entity_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()

    def __str__(self):
        return self.profile.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created=False, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

@receiver(post_save)
def create_profile_reward(sender, instance=None, created=False, **kwargs):
    supported_models = ('Person', 'Movie')
    model_name = sender.__name__
    if model_name in supported_models:
        if created and instance.created_by:
            print([reward for reward in Reward.objects.all()])
            reward = Reward.objects.get(entity_type=model_name[0])
            profile_reward = ProfileReward(profile=instance.created_by, entity_type=model_name[0], entity_data=model_to_dict(instance, fields=[field.name for field in instance._meta.fields]), amount=reward.amount)
            profile_reward.save()