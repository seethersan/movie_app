# Generated by Django 4.0.3 on 2022-03-09 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_movie_created_by_person_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reward',
            name='id',
        ),
        migrations.AlterField(
            model_name='reward',
            name='entity_type',
            field=models.CharField(choices=[('M', 'Movie'), ('P', 'Person')], max_length=1, primary_key=True, serialize=False),
        ),
    ]
