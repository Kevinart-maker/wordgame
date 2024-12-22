from django.urls import path
from . import views

urlpatterns = [
    path('words/', views.word_list, name='word_list'),
    path('content/', views.game_content_list, name='game_content_list'),
]
