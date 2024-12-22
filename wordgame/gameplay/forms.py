from django import forms

class GameSettingsForm(forms.Form):
    difficulty = forms.ChoiceField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    grid_size = forms.IntegerField(min_value=3, max_value=10)
    word_length = forms.IntegerField(min_value=3, max_value=7)