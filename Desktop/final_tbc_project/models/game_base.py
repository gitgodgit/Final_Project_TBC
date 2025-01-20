from abc import ABC, abstractmethod

class WordGame(ABC):
    def __init__(self, player_name):
        self._player_name = player_name
        self._score = 0
        self._is_game_over = False
    
    @abstractmethod
    def start_game(self):
        pass
    
    @abstractmethod
    def make_move(self, move):
        pass
    
    @abstractmethod
    def display_state(self):
        pass
    
    @abstractmethod
    def check_win_condition(self):
        pass
    
    @property
    def score(self):
        return self._score
    
    @property
    def player_name(self):
        return self._player_name
    
    @property
    def is_game_over(self):
        return self._is_game_over
    
    def end_game(self):
        self._is_game_over = True 