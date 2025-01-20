import json
import os

class PlayerData:
    DEFAULT_PLAYER_DATA = {
        "name": "",
        "games_played": 0,
        "wins": 0,
        "losses": 0,
        "hints_used": 0,
        "total_guesses": 0,
        "correct_guesses": 0,
        "current_streak": 0,
        "best_streak": 0,
        "high_score": 0,
        "score": 0
    }
    
    def __init__(self):
        self.file_path = 'player_data.json'
        self.players = self._load_data()
    
    def _load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def _save_data(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.players, file, indent=4)
    
    def get_player_data(self, name):
        if name not in self.players:
            data = self.DEFAULT_PLAYER_DATA.copy()
            data["name"] = name
            return data
        
        player_data = self.players[name]
        for key, value in self.DEFAULT_PLAYER_DATA.items():
            if key not in player_data:
                player_data[key] = value
        
        return player_data
    
    def save_player_stats(self, player_stats):
        name = player_stats["name"]
        
        saved_data = self.get_player_data(name)
        saved_data.update(player_stats)
        
        if "score" in player_stats and player_stats["score"] > saved_data.get("high_score", 0):
            saved_data["high_score"] = player_stats["score"]
        
        self.players[name] = saved_data
        self._save_data()
    
    def get_high_scores(self):
        return sorted(
            [
                {"name": name, "score": data.get("high_score", 0)}
                for name, data in self.players.items()
            ],
            key=lambda x: x["score"],
            reverse=True
        ) 