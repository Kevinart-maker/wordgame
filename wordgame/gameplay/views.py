import string
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Word, GameLevel, GameSession, Score, Achievement, Leaderboard
import random

@login_required
def play_game(request):
    # Get the selected difficulty directly as an integer from the request
    selected_difficulty = request.GET.get('difficulty')

    # If no difficulty is selected, you can either return an error or set a default value
    if selected_difficulty is None:
        selected_difficulty = 1

    try:
        numeric_difficulty = int(selected_difficulty)
    except ValueError:
        return HttpResponse(f"Invalid difficulty level: {selected_difficulty}", status=400)

    game_level = GameLevel.objects.filter(difficulty=numeric_difficulty).first()

    if game_level is None:
        return HttpResponse("No game level found", status=404)

    words = Word.objects.filter(difficulty=numeric_difficulty)  # Use numeric directly
    score = request.session.get('score', 0)
    random_word = None
    result = None

    if 'current_word' in request.session:
        random_word = Word.objects.get(id=request.session['current_word'])
    else:
        random_word = random.choice(words)
        request.session['current_word'] = random_word.id
        request.session['attempts'] = 0
        request.session['streak'] = 0
        request.session['score'] = 0

    # Determine the grid size dynamically based on the word length
    grid_size = determine_grid_size(random_word.word)
    
    # Logic to handle grid generation based on grid size
    grid = create_word_grid(grid_size, random_word.word)

    if request.method == "POST" and random_word:
        user_guess = request.POST.get("user_guess", "").strip()

        if user_guess.lower() == random_word.word.lower():
            score += 10
            request.session['score'] = score
            result = "Correct! Well done."

            if 'streak' not in request.session:
                request.session['streak'] = 0
            
            request.session['streak'] += 1
            check_achievements(request.user, score, request.session)
            save_score(request.user, score)

            random_word = random.choice(words)
            request.session['current_word'] = random_word.id
            request.session['attempts'] = 0
        else:
            request.session['attempts'] += 1
            result = f"Incorrect word. You have {3 - request.session['attempts']} attempts left."

            if request.session['attempts'] >= 3:
                result += f" The correct word was '{random_word.word}'. Try again."
                random_word = random.choice(words)
                request.session['current_word'] = random_word.id
                request.session['attempts'] = 0
                request.session['streak'] = 0

    return render(request, 'gameplay/game.html', {
        'random_word': random_word,
        'grid': grid,
        'result': result,
        'score': score,
        'difficulty': numeric_difficulty,  # Use numeric directly
    })


def determine_grid_size(word):
    # You can customize the grid size based on the length of the word
    return max(len(word) + 2, 5)  # Ensure a minimum grid size of 5

def create_word_grid(grid_size, word):
    print("word:", word)
    # Create an empty grid
    grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Check if the word can fit in the grid
    if len(word) > grid_size:
        raise ValueError("The word is too long to fit in the grid.")
    
    # Determine the position to place the word
    direction = random.choice([0, 1])  # 0 for horizontal, 1 for vertical
    
    # Randomly choose a starting position for the word
    if direction == 0:  # Horizontal
        row = random.randint(0, grid_size - 1)
        col = random.randint(0, grid_size - len(word))  # Ensure the word fits
        for i in range(len(word)):
            grid[row][col + i] = word[i]
    else:  # Vertical
        row = random.randint(0, grid_size - len(word))  # Ensure the word fits
        col = random.randint(0, grid_size - 1)
        for i in range(len(word)):
            grid[row + i][col] = word[i]

    # Fill the remaining empty spaces with random letters
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == '':
                grid[i][j] = random.choice(string.ascii_lowercase)  # Fill with uppercase letters

    return grid

def save_score(user, score):
    leaderboard_entry, created = Leaderboard.objects.get_or_create(user=user)
    if created:
        leaderboard_entry.score = score
    else:
        leaderboard_entry.score += score
    leaderboard_entry.save()

def check_achievements(user, score, session):
    if score >= 50:
        achievement, created = Achievement.objects.get_or_create(
            name='Score 50',
            description='Reach a score of 50 points',
            points=50
        )
        if achievement not in user.achievements.all():
            user.achievements.add(achievement)

    if 'streak' in session and session['streak'] >= 5:
        achievement, created = Achievement.objects.get_or_create(
            name='Word Streak',
            description='Answer 5 words correctly in a row',
            points=50
        )
        if achievement not in user.achievements.all():
            user.achievements.add(achievement)


@login_required
def leaderboard(request):
    leaderboard_entries = Leaderboard.objects.all().order_by('-score')[:10]
    return render(request, 'gameplay/leaderboard.html', {
        'leaderboard_entries': leaderboard_entries,
    })

def home(request):
    return render(request, 'gameplay/home.html')

def contact(request):
    return render(request, 'gameplay/contact.html')