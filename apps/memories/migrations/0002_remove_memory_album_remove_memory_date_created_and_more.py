# Generated by Django 4.2.4 on 2023-09-16 12:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('memories', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memory',
            name='album',
        ),
        migrations.RemoveField(
            model_name='memory',
            name='date_created',
        ),
        migrations.AddField(
            model_name='album',
            name='cover_photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cover_for_albums', to='memories.memory'),
        ),
        migrations.AddField(
            model_name='album',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='album',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='album',
            name='memories',
            field=models.ManyToManyField(blank=True, related_name='albums', to='memories.memory'),
        ),
        migrations.AddField(
            model_name='memory',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
