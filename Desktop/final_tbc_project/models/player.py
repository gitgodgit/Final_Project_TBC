from .player_data import PlayerData

class Player:
    def __init__(self, name):
        self._data_manager = PlayerData()
        saved_data = self._data_manager.get_player_data(name)
        
        self._name = name
        self._wins = saved_data["wins"]
        self._losses = saved_data["losses"]
        self._hints_used = saved_data["hints_used"]
        self._total_guesses = saved_data["total_guesses"]
        self._correct_guesses = saved_data["correct_guesses"]
        self._current_streak = saved_data["current_streak"]
        self._best_streak = saved_data["best_streak"]
        self._games_played = saved_data["games_played"]
        self._score = 0
    
    @property
    def name(self):
        return self._name
    
    @property
    def wins(self):
        return self._wins
    
    @property
    def losses(self):
        return self._losses
    
    @property
    def hints_used(self):
        return self._hints_used
    
    @property
    def current_streak(self):
        return self._current_streak
    
    @property
    def best_streak(self):
        return self._best_streak
    
    @property
    def games_played(self):
        return self._games_played
    
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, value):
        self._score = value
    
    def add_win(self):
        self._wins += 1
        self._games_played += 1
        self._current_streak += 1
        self._best_streak = max(self._current_streak, self._best_streak)
        self._save_stats()
    
    def add_loss(self):
        self._losses += 1
        self._games_played += 1
        self._current_streak = 0
        self._save_stats()
    
    def add_guess(self, correct=False):
        self._total_guesses += 1
        if correct:
            self._correct_guesses += 1
        self._save_stats()
    
    def use_hint(self):
        self._hints_used += 1
        self._save_stats()
    
    def get_win_rate(self):
        if self._games_played == 0:
            return 0
        return (self._wins / self._games_played) * 100
    
    def get_guess_accuracy(self):
        if self._total_guesses == 0:
            return 0
        return (self._correct_guesses / self._total_guesses) * 100
    
    def get_stats(self):
        stats = {
            "name": self._name,
            "games_played": self._games_played,
            "wins": self._wins,
            "losses": self._losses,
            "win_rate": f"{self.get_win_rate():.1f}%",
            "current_streak": self._current_streak,
            "best_streak": self._best_streak,
            "hints_used": self._hints_used,
            "guess_accuracy": f"{self.get_guess_accuracy():.1f}%",
            "score": self._score
        }
        return stats
    
    def _save_stats(self):
        self._data_manager.save_player_stats(self.get_stats()) 