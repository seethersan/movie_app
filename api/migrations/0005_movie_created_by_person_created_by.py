# Generated by Django 4.0.3 on 2022-03-09 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_profile_reward_profilereward'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.profile'),
        ),
        migrations.AddField(
            model_name='person',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.profile'),
        ),
    ]
