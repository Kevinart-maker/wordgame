# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    current_level = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    achievements = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)

class Word(models.Model):
    word = models.CharField(max_length=100)
    definition = models.TextField()

    def __str__(self):
        return self.word

class GameContent(models.Model):
    content_type = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.content_type
