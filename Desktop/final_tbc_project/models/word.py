import json
import random

class Word:
    def __init__(self):
        self._words_data = self.load_words()
        self._word = ""
        self._hint = ""
        self._category = ""
        self._masked_word = []
        self._difficulty = 0
    
    @property
    def word(self):
        return self._word
    
    @property
    def hint(self):
        return self._hint
    
    @property
    def category(self):
        return self._category
    
    @property
    def difficulty(self):
        return self._difficulty
    
    def load_words(self):
        try:
            with open('words.json', 'r') as file:
                data = json.load(file)
                return data['words']
        except FileNotFoundError:
            print("Error: words.json file not found!")
            exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in words.json!")
            exit(1)
    
    def select_word(self, difficulty=1):
        self._difficulty = difficulty
        eligible_words = [w for w in self._words_data 
                         if (difficulty == 1 and len(w['word']) <= 6) or
                            (difficulty == 2 and 6 < len(w['word']) <= 8) or
                            (difficulty == 3 and len(w['word']) > 8)]
        
        if not eligible_words:
            eligible_words = self._words_data
        
        word_data = random.choice(eligible_words)
        self._word = word_data['word'].lower()
        self._hint = word_data['hint']
        self._masked_word = ['_'] * len(self._word)
    
    def get_display_word(self):
        return ' '.join(self._masked_word)
    
    def reveal_letter(self, letter):
        letter = letter.lower()
        found = False
        for i, char in enumerate(self._word):
            if char == letter:
                self._masked_word[i] = letter
                found = True
        return found
    
    def is_complete(self):
        return '_' not in self._masked_word
    
    def get_random_hint(self):
        unrevealed_indices = [i for i, char in enumerate(self._masked_word) if char == '_']
        if unrevealed_indices:
            random_index = random.choice(unrevealed_indices)
            return self._word[random_index]
        return None
    
    def get_word_length(self):
        return len(self._word)
    
    def get_remaining_letters(self):
        return len([c for c in self._masked_word if c == '_']) 