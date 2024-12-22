from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Word model
class Word(models.Model):
    word = models.CharField(max_length=100, unique=True)
    definition = models.TextField()
    difficulty = models.IntegerField(default=1)

    def __str__(self):
        return self.word

# GameLevel model
class GameLevel(models.Model):
    level_name = models.CharField(max_length=20)
    difficulty = models.IntegerField()
    grid_size = models.IntegerField(default=4)  # Add grid size
    word_length = models.IntegerField(default=4)  # Add word length

    def __str__(self):
        return f"{self.level_name} (Grid: {self.grid_size}x{self.grid_size})"

# GameSession model
class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(GameLevel, on_delete=models.CASCADE)
    current_word = models.ForeignKey(Word, on_delete=models.SET_NULL, null=True)
    score = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)
    date_started = models.DateTimeField(auto_now_add=True)

# Score model
class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.score}"
    
class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name

# Leaderboard model
class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date_achieved = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return f"{self.user.username}: {self.score}"