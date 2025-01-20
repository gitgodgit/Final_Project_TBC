from game import HangmanGame
from models.player_data import PlayerData

def get_player_name():
    while True:
        name = input("\nPlease enter your name❤️ : ").strip()
        if name and all(c.isalpha() or c.isspace() for c in name):
            return name
        print("Please enter a valid name (letters and spaces only)")

def display_high_scores():
    data_manager = PlayerData()
    high_scores = data_manager.get_high_scores()
    
    print("\n🏆 High Scores:")
    print("-" * 30)
    print("🏅 Rank  Player          Score")
    print("-" * 30)
    
    medals = ["🥇", "🥈", "🥉", "✨", "✨"]
    for i, score in enumerate(high_scores[:5], 1):
        print(f"{medals[i-1]} {i:2d}  {score['name']:<15} {score['score']:5d}")
    print("-" * 30)

def main():
    print("\n" * 5)
    print("🎮 === HANGMAN GAME === 🎮")
    print("\n✨ Features:")
    print("🎮 Three difficulty levels")
    print("💡 Hints available (3 per game)")
    print("📊 Player statistics tracking")
    print("⏱️  Time tracking")
    print("📚 Various word categories")
    print("🏆 Persistent high scores")
    
    player_name = get_player_name()
    game = HangmanGame(player_name)
    
    print(f"\n👋 Welcome back, {player_name}!")
    display_high_scores()
    
    while True:
        if not game.play_round():
            break
        
        display_high_scores()
        play_again = input(f"\n🎮 {player_name}, would you like to play again? (y/n): ").lower()
        if play_again != 'y':
            break
    
    print("\n📊 Final Statistics:")
    game.display_stats()
    display_high_scores()
    print(f"\n👋 Thanks for playing, {player_name}! 🎮")

if __name__ == "__main__":
    main() 