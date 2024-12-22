from django.urls import path
from . import views

urlpatterns = [
    path('play/', views.play_game, name='play_game'),
    path('leaderboard/', views.leaderboard, name='leaderboard'), 
    path('contact/', views.contact, name='contact'), 
    path('', views.home, name='home'),
]