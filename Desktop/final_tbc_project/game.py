import os
import time
from models.word import Word
from models.player import Player
from models.game_base import WordGame

class HangmanGame(WordGame):
    HANGMAN_STAGES = [
        '''
        🌳
        🟦
        🟦
        🟦
        🟦
        🟫
        ''',
        '''
        🌳
        🟦  😊
        🟦
        🟦
        🟦
        🟫
        ''',
        '''
        🌳
        🟦  😊
        🟦  👕
        🟦
        🟦
        🟫
        ''',
        '''
        🌳
        🟦  😊
        🟦  👕
        🟦  🤚
        🟦
        🟫
        ''',
        '''
        🌳
        🟦  😅
        🟦  👕
        🟦 🤚✋
        🟦
        🟫
        ''',
        '''
        🌳
        🟦  😰
        🟦  👕
        🟦 🤚✋
        🟦  👞
        🟫
        ''',
        '''
        🌳
        🟦  💀
        🟦  👕
        🟦 🤚✋
        🟦 👞👞
        🟫
        '''
    ]
    
    DIFFICULTY_LEVELS = {
        1: "Easy (words up to 6 letters)",
        2: "Medium (words 7-8 letters)",
        3: "Hard (words 9+ letters)"
    }
    
    def __init__(self, player_name):
        super().__init__(player_name)
        self._word = Word()
        self._player = Player(player_name)
        self._remaining_attempts = 6
        self._guessed_letters = set()
        self._start_time = None
        self._hints_remaining = 3
        self._difficulty = 1
    
    @property
    def remaining_attempts(self):
        return self._remaining_attempts
    
    @property
    def hints_remaining(self):
        return self._hints_remaining
    
    @property
    def difficulty(self):
        return self._difficulty
    
    def select_difficulty(self):
        print("\n🎮 Select difficulty level:")
        for level, desc in self.DIFFICULTY_LEVELS.items():
            emoji = "🟢" if level == 1 else "🟡" if level == 2 else "🔴"
            print(f"{emoji} {level}. {desc}")
        
        while True:
            try:
                choice = int(input("\n🎯 Enter difficulty (1-3): "))
                if 1 <= choice <= 3:
                    self._difficulty = choice
                    break
                print("⚠️  Please enter a number between 1 and 3")
            except ValueError:
                print("⚠️  Please enter a valid number")
    
    def start_game(self):
        self.select_difficulty()
        self._word.select_word(self._difficulty)
        self._remaining_attempts = 6
        self._guessed_letters = set()
        self._start_time = time.time()
    
    def use_hint(self):
        if self._hints_remaining > 0:
            letter = self._word.get_random_hint()
            if letter:
                self._hints_remaining -= 1
                self._player.use_hint()
                self._guessed_letters.add(letter)
                self._word.reveal_letter(letter)
                return f"Revealed letter: {letter}"
            return "No more letters to reveal!"
        return "No hints remaining!"
    
    def display_state(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n👤 Player: {self._player.name}")
        print(f"🎯 Difficulty: {self.DIFFICULTY_LEVELS[self._difficulty]}")
        hint_status = "✨" * self._hints_remaining + "❌" * (3 - self._hints_remaining)
        print(f"💡 Hints: {hint_status} ({self._hints_remaining} remaining)")
        print(self.HANGMAN_STAGES[6 - self._remaining_attempts])
        print(f"\n📝 Word: {self._word.get_display_word()}")
        print(f"🔍 Hint: {self._word.hint}")
        print(f"🔤 Guessed letters: {', '.join(sorted(self._guessed_letters)) if self._guessed_letters else 'None'}")
        print(f"❤️  Remaining attempts: {self._remaining_attempts}")
        elapsed_time = int(time.time() - self._start_time)
        print(f"⏱️  Time elapsed: {elapsed_time // 60}:{elapsed_time % 60:02d}")
    
    def make_move(self, guess):
        if guess in self._guessed_letters:
            return f"\n❌ {self._player.name}, you already guessed that letter!"
        
        self._guessed_letters.add(guess)
        
        if self._word.reveal_letter(guess):
            self._player.add_guess(correct=True)
            self._score += 10 * self._difficulty
            self._player.score = self._score
            return f"\n✅ Good job, {self._player.name}! That's correct!"
        else:
            self._remaining_attempts -= 1
            self._player.add_guess(correct=False)
            return f"\n☠️ Sorry {self._player.name}, that's incorrect!"
    
    def check_win_condition(self):
        if self._word.is_complete():
            self._player.add_win()
            if self._player.get_stats()["current_streak"] >= 2:
                self._hints_remaining += 1
                return f"🎉 Win! You got a streak of {self._player.get_stats()['current_streak']}! Bonus hint awarded! 💡"
            return True
        if self._remaining_attempts <= 0:
            self._player.add_loss()
            return True
        return False
    
    def display_stats(self):
        stats = self._player.get_stats()
        print("\n📊 Player Statistics:")
        print("-" * 20)
        for key, value in stats.items():
            if key == "wins":
                print(f"🏆 {key.replace('_', ' ').title()}: {value}")
            elif key == "losses":
                print(f"💔 {key.replace('_', ' ').title()}: {value}")
            elif key == "score":
                print(f"🎯 {key.replace('_', ' ').title()}: {value}")
            elif key == "high_score":
                print(f"🏅 {key.replace('_', ' ').title()}: {value}")
            elif key == "current_streak":
                print(f"🔥 {key.replace('_', ' ').title()}: {value}")
            elif key == "best_streak":
                print(f"⭐ {key.replace('_', ' ').title()}: {value}")
            elif key == "hints_used":
                print(f"💡 {key.replace('_', ' ').title()}: {value}")
            elif key == "guess_accuracy":
                print(f"🎯 {key.replace('_', ' ').title()}: {value}")
            else:
                print(f"📈 {key.replace('_', ' ').title()}: {value}")
    
    def play_round(self):
        self.start_game()
        
        while not self.is_game_over:
            self.display_state()
            
            if self._word.is_complete():
                print(f"\n🎉 Congratulations {self._player.name}! You won! 🏆")
                print(f"🎯 The word was: {self._word.word}")
                self._player.add_win()
                self.display_stats()
                return True
            
            if self._remaining_attempts <= 0:
                print(f"\n☠️ Game Over {self._player.name}! The word was: {self._word.word} ☠️")
                self._player.add_loss()
                self.display_stats()
                return True
            
            hint_text = "'hint' for a hint 💡, " if self._hints_remaining > 0 else ""
            action = input(f"\n👉 {self._player.name}, enter a letter, {hint_text}or 'quit' to exit: ").lower()
            
            if action == 'quit':
                return False
            elif action == 'hint':
                if self._hints_remaining > 0:
                    print(self.use_hint())
                else:
                    print("\n❌ No hints remaining! You've used all 3 hints! 🚫")
                continue
            elif not action.isalpha() or len(action) != 1:
                print(f"\n⚠️  {self._player.name}, please enter a single letter!")
                continue
            
            result = self.make_move(action)
            print(result) 
