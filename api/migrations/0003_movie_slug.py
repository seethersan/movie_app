# Generated by Django 4.0.3 on 2022-03-02 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_role_movie_alter_role_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
