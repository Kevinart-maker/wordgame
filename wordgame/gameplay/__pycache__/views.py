from django.shortcuts import render
from .models import Word, GameContent

def word_list(request):
    words = Word.objects.all()
    return render(request, 'word_list.html', {'words': words})

def game_content_list(request):
    contents = GameContent.objects.all()
    return render(request, 'game_content_list.html', {'contents': contents})
