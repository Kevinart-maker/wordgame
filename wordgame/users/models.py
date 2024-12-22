from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    current_level = models.IntegerField(default=1)  # Tracks the current level user is on
    total_score = models.IntegerField(default=0)  # Cumulative score
    achievements = models.ManyToManyField('gameplay.Achievement', related_name="users", blank=True)  # Proper ManyToMany relation for achievements
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username