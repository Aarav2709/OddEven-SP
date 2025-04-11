import json
import random
import sys
from typing import Dict, List, Tuple, Optional

# Constants
BAT = 'bat'
BOWL = 'bowl'
DIFFICULTIES = ['easy', 'medium', 'hard']
ACHIEVEMENTS_FILE = "achievements.json"
STATS_FILE = "player_stats.json"
MAX_SCORE = 10
MIN_SCORE = 1

# Rank System
RANKS = [
    "Warrior", "Titan", "Blaster", "Striker", "Smasher", "Dynamo",
    "Majestic", "Maverick", "Mighty", "Crusher", "Champion"
]

class GameState:
    def __init__(self):
        self.player_stats = {
            "wins": 0,
            "losses": 0,
            "total_score": 0,
            "level": 1,
            "xp": 0,
            "rank_points": 0,
            "rank": "Warrior"
        }
        self.achievements = {
            "Score 50 Runs in a Game": False,
            "Score 100 Runs in a Game": False,
            "Win 3 Games in a Row": False,
            "Win a Game on Hard": False,
            "Win Without Getting Out": False
        }
        self.consecutive_wins = 0
        self.mode = 'dark'
        self.player_history = []
        self.colors = {
            'dark': {'red': '\033[91m', 'green': '\033[92m', 'yellow': '\033[93m', 
                    'blue': '\033[94m', 'magenta': '\033[95m', 'cyan': '\033[96m', 
                    'reset': '\033[0m'},
            'light': {'red': '\033[31m', 'green': '\033[32m', 'yellow': '\033[33m', 
                     'blue': '\033[34m', 'magenta': '\033[35m', 'cyan': '\033[36m', 
                     'reset': '\033[0m'}
        }

    def colored(self, text: str, color: str) -> str:
        """Return colored text based on the selected mode."""
        return f"{self.colors[self.mode].get(color, self.colors[self.mode]['reset'])}{text}{self.colors[self.mode]['reset']}"

    def load_data(self):
        """Load game data from files."""
        try:
            with open(ACHIEVEMENTS_FILE, "r") as file:
                self.achievements = json.load(file)
            with open(STATS_FILE, "r") as file:
                self.player_stats = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Use defaults if files don't exist or are corrupt

    def save_data(self):
        """Save game data to files."""
        try:
            with open(ACHIEVEMENTS_FILE, "w") as file:
                json.dump(self.achievements, file)
            with open(STATS_FILE, "w") as file:
                json.dump(self.player_stats, file)
        except IOError as e:
            print(self.colored(f"Error saving data: {e}", 'red'))

    def get_valid_input(self, prompt: str, valid_options: List[str]) -> str:
        """Get validated user input."""
        while True:
            user_input = input(self.colored(prompt, 'yellow')).strip().lower()
            if user_input in valid_options:
                return user_input
            print(self.colored(f"Invalid choice! Please choose from: {', '.join(valid_options)}", 'red'))

    def choose_mode(self):
        """Let the user choose between dark and light mode."""
        self.mode = self.get_valid_input(
            "Choose your mode: 'light' or 'dark' 🌞🌚: ", 
            ['light', 'dark']
        )

    def progress_bar(self, current: int, target: int, length: int = 20) -> str:
        """Display a progress bar."""
        progress = min(int((current / target) * length), length)
        percentage = min(int((current / target) * 100), 100)
        color = 'green' if percentage >= 70 else 'yellow' if percentage >= 40 else 'red'
        bar = f"[{'█' * progress}{' ' * (length - progress)}] {percentage}%"
        return f"Progress: {self.colored(bar, color)}"

    def toss(self) -> str:
        """Simulate a coin toss."""
        print(self.colored("\nToss Time! Choose Heads or Tails 🍀", 'cyan'))
        choice = self.get_valid_input("Enter 'Heads' or 'Tails': 🪙", ['heads', 'tails'])
        result = random.choice(['heads', 'tails'])
        print(f"\n{self.colored(f'Toss Result: {result.capitalize()} 🎯', 'magenta')}")

        if choice == result:
            print(self.colored("\nYou won the toss! 🎉", 'green'))
            return self.get_valid_input(
                "\nDo you want to Bat 🏏 or Bowl 🏆 first? (Enter 'bat' or 'bowl'): ", 
                [BAT, BOWL]
            )
        print(self.colored("\nYou lost the toss! Opponent will bowl first. 🏏", 'red'))
        return BOWL

    def player_turn(self) -> int:
        """Get valid player input for their turn."""
        while True:
            try:
                player_input = int(input("Enter a number between 1 and 10: "))
                if MIN_SCORE <= player_input <= MAX_SCORE:
                    self.player_history.append(player_input)
                    return player_input
                print(f"Please enter a number between {MIN_SCORE} and {MAX_SCORE}.")
            except ValueError:
                print("Invalid input! Please enter an integer.")

    def get_computer_input(self, difficulty: str, player_input: Optional[int] = None, 
                          user_score: int = 0, computer_score: int = 0) -> int:
        """Generate computer's move based on difficulty."""
        if difficulty == 'easy':
            return random.randint(MIN_SCORE, MAX_SCORE)
        
        elif difficulty == 'medium':
            comp_input = random.randint(MIN_SCORE, MAX_SCORE)
            while player_input and comp_input == player_input:
                comp_input = random.randint(MIN_SCORE, MAX_SCORE)
            return comp_input
        
        elif difficulty == 'hard':
            if len(self.player_history) >= 3:
                predicted = max(set(self.player_history[-3:]), key=self.player_history[-3:].count)
            else:
                predicted = random.randint(MIN_SCORE, MAX_SCORE)
            
            if computer_score < user_score:
                return random.choice([predicted, (predicted + 1) % (MAX_SCORE + 1) or MAX_SCORE])
            return random.choice([predicted, (predicted - 1) % (MAX_SCORE + 1) or MIN_SCORE])
        
        return random.randint(MIN_SCORE, MAX_SCORE)

    def update_stats(self, score: int, outcome: str) -> Tuple[int, int]:
        """Update player stats and return XP and RP gained."""
        xp_gained = score * 10
        self.player_stats["xp"] += xp_gained
        xp_required = int(100 * (self.player_stats["level"] ** 1.5))

        while self.player_stats["xp"] >= xp_required:
            self.player_stats["level"] += 1
            self.player_stats["xp"] -= xp_required
            xp_required = int(100 * (self.player_stats["level"] ** 1.5))
            print(self.colored(f"Level Up! You are now Level {self.player_stats['level']} 🎉", 'green'))

        rp_gained = 20 if outcome == "win" else -10
        self.player_stats["rank_points"] = max(0, self.player_stats["rank_points"] + rp_gained)
        
        rank_index = RANKS.index(self.player_stats["rank"])
        if rank_index < len(RANKS) - 1 and self.player_stats["rank_points"] >= 100:
            self.player_stats["rank"] = RANKS[rank_index + 1]
            self.player_stats["rank_points"] = 0
            print(self.colored(f"Rank Up! You are now a {self.player_stats['rank']} 🎉", 'green'))
        elif rank_index > 0 and self.player_stats["rank_points"] < 0:
            self.player_stats["rank"] = RANKS[rank_index - 1]
            self.player_stats["rank_points"] = 50
            print(self.colored(f"Rank Down! You are now a {self.player_stats['rank']} 💔", 'red'))

        return xp_gained, rp_gained

    def check_achievements(self, score: int, difficulty: str, perfect_win: bool):
        """Check and unlock achievements."""
        if score >= 50 and not self.achievements["Score 50 Runs in a Game"]:
            self.achievements["Score 50 Runs in a Game"] = True
            print(self.colored("Achievement Unlocked: Score 50 Runs in a Game! 🏅", 'green'))
        
        if score >= 100 and not self.achievements["Score 100 Runs in a Game"]:
            self.achievements["Score 100 Runs in a Game"] = True
            print(self.colored("Achievement Unlocked: Score 100 Runs in a Game! 🏅", 'green'))
        
        if self.consecutive_wins >= 3 and not self.achievements["Win 3 Games in a Row"]:
            self.achievements["Win 3 Games in a Row"] = True
            print(self.colored("Achievement Unlocked: Win 3 Games in a Row! 🏅", 'green'))
        
        if difficulty == 'hard' and not self.achievements["Win a Game on Hard"]:
            self.achievements["Win a Game on Hard"] = True
            print(self.colored("Achievement Unlocked: Win a Game on Hard! 🏅", 'green'))
        
        if perfect_win and not self.achievements["Win Without Getting Out"]:
            self.achievements["Win Without Getting Out"] = True
            print(self.colored("Achievement Unlocked: Win Without Getting Out! 🏅", 'green'))
        
        print(self.colored(f"Current Win Streak: {self.consecutive_wins} 🏅", 'cyan'))

    def play_innings(self, batting: str, difficulty: str, target: Optional[int] = None) -> Tuple[int, bool]:
        """Play one innings of the game."""
        score = 0
        player_batting = batting == 'player'
        perfect = True
        
        while True:
            player_input = self.player_turn()
            comp_input = self.get_computer_input(
                difficulty, 
                player_input if player_batting else None,
                score if player_batting else 0,
                0 if player_batting else score
            )
            
            print(f"\nComputer chose: {self.colored(comp_input, 'cyan')} 🤖")
            
            if player_input == comp_input:
                print(self.colored("\nOut! Innings over. 🛑", 'red'))
                perfect = False
                break
                
            score += player_input if player_batting else comp_input
            print(f"Current score: {self.colored(score, 'green' if player_batting else 'red')} "
                  f"{'🏏' if player_batting else '⚡'}")
            
            if target and score > target:
                break
                
        return score, perfect

    def play_game(self):
        """Main game loop."""
        print(self.colored("\nWelcome to the Odd-Even Game!", 'blue'))
        print(self.colored("Rules: Choose numbers 1-10. Match means out!", 'yellow'))

        difficulty = self.get_valid_input(
            "\nChoose difficulty (easy/medium/hard): ⚡", 
            DIFFICULTIES
        )
        
        decision = self.toss()
        player_score, comp_score = 0, 0
        perfect_win = False

        if decision == BAT:
            print(self.colored("\nYou're batting first! 🏏", 'green'))
            player_score, _ = self.play_innings('player', difficulty)
            print(self.colored(f"\nYour total: {player_score} 🏆", 'green'))
            
            print(self.colored("\nNow bowling! 🏏", 'magenta'))
            comp_score, _ = self.play_innings('computer', difficulty, player_score)
            
            if comp_score <= player_score:
                self.player_stats["wins"] += 1
                self.player_stats["total_score"] += player_score
                self.consecutive_wins += 1
                xp, rp = self.update_stats(player_score, "win")
                print(self.colored("\nYou win! 🎉", 'green'))
                perfect_win = comp_score < player_score
            else:
                self.player_stats["losses"] += 1
                self.consecutive_wins = 0
                xp, rp = self.update_stats(player_score, "loss")
                print(self.colored("\nComputer wins! 💔", 'red'))
        else:
            print(self.colored("\nComputer is batting first! 🏏", 'magenta'))
            comp_score, _ = self.play_innings('computer', difficulty)
            print(self.colored(f"\nComputer's total: {comp_score} ⚡", 'red'))
            
            print(self.colored("\nNow batting! 🏏", 'green'))
            player_score, perfect = self.play_innings('player', difficulty, comp_score)
            
            if player_score > comp_score:
                self.player_stats["wins"] += 1
                self.player_stats["total_score"] += player_score
                self.consecutive_wins += 1
                xp, rp = self.update_stats(player_score, "win")
                print(self.colored("\nYou win! 🎉", 'green'))
                perfect_win = perfect
            else:
                self.player_stats["losses"] += 1
                self.consecutive_wins = 0
                xp, rp = self.update_stats(player_score, "loss")
                print(self.colored("\nComputer wins! 💔", 'red'))

        # Match summary
        print(self.colored("\n--- Match Summary --- 📜", 'blue'))
        print(f"Difficulty: {self.colored(difficulty.capitalize(), 'yellow')} ⚡")
        print(f"Your Score: {self.colored(player_score, 'green')} 🏆")
        print(f"Computer Score: {self.colored(comp_score, 'red')} ⚡")
        
        xp_needed = int(100 * (self.player_stats["level"] ** 1.5))
        print(self.colored("\nPlayer Stats:", 'cyan'))
        print(f"Level: {self.player_stats['level']} [{self.player_stats['xp']}/{xp_needed} XP] +{xp} XP")
        print(f"Rank: {self.player_stats['rank']} [{self.player_stats['rank_points']}/100 RP] +{rp} RP")
        print(f"Wins: {self.colored(self.player_stats['wins'], 'green')} 🏆")
        print(f"Losses: {self.colored(self.player_stats['losses'], 'red')} ⚡")
        print(f"Total Score: {self.colored(self.player_stats['total_score'], 'yellow')} 💯")

        self.check_achievements(player_score, difficulty, perfect_win)
        self.save_data()

def main():
    game = GameState()
    game.load_data()
    game.choose_mode()
    
    bot_names = ['Fankara', 'Lobamgi', 'Fola', 'Das', 'James', 'Rad']
    bot_countries = ['West Indies', 'India', 'Australia', 'England']
    
    print(game.colored(
        f"\nPlayer: {input('Enter your name: ')} ({input('Enter your country: ')}) vs "
        f"{random.choice(bot_names)} ({random.choice(bot_countries)}) 🏆",
        'blue'
    ))

    while True:
        game.play_game()
        if game.get_valid_input("\nPlay again? (yes/no): 🌟", ['yes', 'no']) == 'no':
            print(game.colored("\nThanks for playing! Goodbye! ✌️", 'magenta'))
            break

if __name__ == "__main__":
    main()