import json
import random
from typing import Dict, List, Tuple, Optional
from enum import Enum
import colorama
from colorama import Fore, Back, Style
import time

# Initialize colorama
colorama.init(autoreset=True)

# ========== Constants ========== #
class GameMode(Enum):
    BAT = 'bat'
    BOWL = 'bowl'

class Difficulty(Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'

MAX_SCORE = 10
MIN_SCORE = 1
BASE_XP = 100
XP_SCALING = 1.5
ACHIEVEMENTS_FILE = "achievements.json"
STATS_FILE = "player_stats.json"

RANKS = [
    "Rookie", "Warrior", "Titan", "Blaster", "Striker", 
    "Smasher", "Dynamo", "Majestic", "Maverick", "Champion"
]

THEMES = {
    'dark': {
        'text': Fore.WHITE,
        'primary': Fore.CYAN,
        'success': Fore.GREEN,
        'warning': Fore.YELLOW,
        'danger': Fore.RED,
        'highlight': Fore.MAGENTA
    },
    'light': {
        'text': Fore.BLACK,
        'primary': Fore.BLUE,
        'success': Fore.GREEN,
        'warning': Fore.YELLOW,
        'danger': Fore.RED,
        'highlight': Fore.MAGENTA
    },
    'neon': {
        'text': Fore.WHITE,
        'primary': Fore.LIGHTCYAN_EX,
        'success': Fore.LIGHTGREEN_EX,
        'warning': Fore.LIGHTYELLOW_EX,
        'danger': Fore.LIGHTRED_EX,
        'highlight': Fore.LIGHTMAGENTA_EX
    }
}

# ========== Bot System ========== #
class CricketBot:
    def __init__(self):
        self.personalities = {
            'aggressive': {
                'bat_style': 'attack',
                'bowl_style': 'attack',
                'taunts': ["I'll smash you!", "Too easy!", "Boring!"],
                'compliments': ["Not bad.", "Lucky shot!", "Hmph!"],
                'win_phrases': ["I told you I'm the best!", "Better luck next time!"],
                'lose_phrases': ["You got lucky!", "I'll get you next time!"]
            },
            'defensive': {
                'bat_style': 'defend',
                'bowl_style': 'defend',
                'taunts': ["You can't break me!", "I'm unbreakable!", "Try harder!"],
                'compliments': ["Good try.", "Nice move", "Interesting."],
                'win_phrases': ["Defense wins games!", "Solid victory!"],
                'lose_phrases': ["Close match.", "Almost had it!"]
            },
            'tricky': {
                'bat_style': 'mix',
                'bowl_style': 'mix',
                'taunts': ["Can you read me?", "Guess what's coming!", "I'm unpredictable!"],
                'compliments': ["You guessed right!", "Good read!", "Hmm."],
                'win_phrases': ["Mind games win!", "Outplayed!"],
                'lose_phrases': ["You read me well.", "Next time will be different!"]
            }
        }
        self.name = random.choice(['Fankara', 'Lobamgi', 'Fola', 'Das', 'James', 'Rad'])
        self.country = random.choice(['West Indies', 'India', 'Australia', 'England'])
        self.personality = random.choice(list(self.personalities.keys()))
        self.mood = 'neutral'
        
    def get_taunt(self) -> str:
        return random.choice(self.personalities[self.personality]['taunts'])
    
    def get_compliment(self) -> str:
        return random.choice(self.personalities[self.personality]['compliments'])
    
    def get_win_phrase(self) -> str:
        return random.choice(self.personalities[self.personality]['win_phrases'])
    
    def get_lose_phrase(self) -> str:
        return random.choice(self.personalities[self.personality]['lose_phrases'])
    
    def react(self, situation: str):
        if situation == 'good_move':
            print(f"\n{self.name}: {self.get_compliment()}")
        elif situation == 'bad_move':
            print(f"\n{self.name}: {self.get_taunt()}")
        time.sleep(0.5)

    def describe(self) -> str:
        desc = f"{self.name} from {self.country} - {self.personality.capitalize()} style"
        if self.personality == 'aggressive':
            return f"🔥 {desc} (Loves big hits)"
        elif self.personality == 'defensive':
            return f"🛡️ {desc} (Strong defense)"
        else:
            return f"🎭 {desc} (Unpredictable)"

# ========== Helper Classes ========== #
class PlayerStats:
    def __init__(self):
        self.wins: int = 0
        self.losses: int = 0
        self.ties: int = 0
        self.total_score: int = 0
        self.high_score: int = 0
        self.level: int = 1
        self.xp: int = 0
        self.rank_points: int = 0
        self.rank: str = RANKS[0]
        self.streak: int = 0
        self.games_played: int = 0
        self.rivalries: Dict[str, int] = {}

    def to_dict(self) -> Dict:
        return {
            'wins': self.wins,
            'losses': self.losses,
            'ties': self.ties,
            'total_score': self.total_score,
            'high_score': self.high_score,
            'level': self.level,
            'xp': self.xp,
            'rank_points': self.rank_points,
            'rank': self.rank,
            'streak': self.streak,
            'games_played': self.games_played,
            'rivalries': self.rivalries
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'PlayerStats':
        stats = cls()
        for key, value in data.items():
            setattr(stats, key, value)
        return stats

class AchievementManager:
    def __init__(self):
        self.achievements = {
            "50 Run Blitz": False,
            "Centurion": False,
            "Hat-Trick Hero": False,
            "Hard Mode Champion": False,
            "Flawless Victory": False,
            "Veteran Player": False,
            "Rivalry Settled": False,
            "Style Master": False,
            "Comeback King": False
        }

    def unlock(self, achievement: str) -> bool:
        if achievement in self.achievements and not self.achievements[achievement]:
            self.achievements[achievement] = True
            return True
        return False

    def to_dict(self) -> Dict:
        return self.achievements

    @classmethod
    def from_dict(cls, data: Dict) -> 'AchievementManager':
        manager = cls()
        manager.achievements = data
        return manager

# ========== Main Game Class ========== #
class OddEvenGame:
    def __init__(self):
        self.stats = PlayerStats()
        self.achievements = AchievementManager()
        self.theme = 'dark'
        self.player_history: List[int] = []
        self.player_name: str = ""
        self.player_country: str = ""
        self.bot = CricketBot()
        self.load_game_data()

    def color_text(self, text: str, color_type: str) -> str:
        color = THEMES[self.theme].get(color_type, THEMES[self.theme]['text'])
        return f"{color}{text}{Style.RESET_ALL}"

    def print_header(self, text: str):
        print(f"\n{self.color_text('═' * 50, 'primary')}")
        print(self.color_text(f"{text:^50}", 'highlight'))
        print(f"{self.color_text('═' * 50, 'primary')}\n")

    def progress_bar(self, current: int, target: int, length: int = 20) -> str:
        """Fixed progress bar that works for all scenarios"""
        if target <= 0:
            return f"[{' ' * length}] 0%"
        
        progress = min(current / target, 1.0)
        filled = int(progress * length)
        bar = '█' * filled + ' ' * (length - filled)
        percentage = int(progress * 100)
        
        if current >= target:
            color = 'success'
        elif percentage >= 70:
            color = 'warning'
        else:
            color = 'danger'
            
        return f"[{bar}] {percentage}%"

    def load_game_data(self):
        try:
            with open(STATS_FILE, 'r') as f:
                self.stats = PlayerStats.from_dict(json.load(f))
            with open(ACHIEVEMENTS_FILE, 'r') as f:
                self.achievements = AchievementManager.from_dict(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_game_data(self):
        try:
            with open(STATS_FILE, 'w') as f:
                json.dump(self.stats.to_dict(), f)
            with open(ACHIEVEMENTS_FILE, 'w') as f:
                json.dump(self.achievements.to_dict(), f)
        except IOError as e:
            print(self.color_text(f"Error saving game data: {e}", 'danger'))

    def get_valid_input(self, prompt: str, valid_options: List[str], max_attempts: int = 3) -> str:
        attempts = 0
        while attempts < max_attempts:
            user_input = input(self.color_text(prompt, 'warning')).strip().lower()
            if user_input in valid_options:
                return user_input
            attempts += 1
            print(self.color_text(f"Invalid input! Please choose from: {', '.join(valid_options)}", 'danger'))
        return valid_options[0]

    def simulate_toss(self) -> GameMode:
        """Fair toss with true 50-50 chance"""
        self.print_header("Toss Time!")
        print(f"{self.bot.name}: \"Let's see who gets the advantage!\"")
        time.sleep(1)
        
        choice = self.get_valid_input("Choose heads or tails: ", ['heads', 'tails'])
        result = random.choice(['heads', 'tails'])
        
        print(f"\n{self.color_text(f'» The coin lands on... {result.capitalize()}!', 'primary')}")
        time.sleep(1)
        
        if choice == result:
            print(self.color_text("\n» You won the toss! 🎉", 'success'))
            print(f"{self.bot.name}: \"Lucky toss...\"")
            time.sleep(1)
            decision = self.get_valid_input(
                "Do you want to (B)at or (B)owl first? ", 
                ['b', 'bat', 'bowl']
            )
            return GameMode.BAT if decision.startswith('b') and decision != 'bowl' else GameMode.BOWL
        
        print(self.color_text("\n» You lost the toss!", 'danger'))
        # 50-50 chance for bot to choose bat or bowl
        bot_choice = random.choice([GameMode.BAT, GameMode.BOWL])
        print(f"{self.bot.name}: \"I'll choose to {bot_choice.value} first!\"")
        time.sleep(1)
        return bot_choice

    def get_player_move(self) -> int:
        while True:
            try:
                move = int(input(self.color_text("Enter your move (1-10): ", 'warning')))
                if MIN_SCORE <= move <= MAX_SCORE:
                    self.player_history.append(move)
                    return move
                print(self.color_text(f"Please enter between {MIN_SCORE}-{MAX_SCORE}", 'danger'))
            except ValueError:
                print(self.color_text("Invalid input! Please enter a number.", 'danger'))

    def get_computer_move(self, difficulty: Difficulty, is_batting: bool, player_score: int = 0, target: Optional[int] = None) -> int:
        """Properly balanced difficulty system"""
        # Base move is always random between min and max
        base_move = random.randint(MIN_SCORE, MAX_SCORE)
        
        if difficulty == Difficulty.EASY:
            # Easy mode - completely random, sometimes makes bad moves
            if random.random() < 0.4:  # 40% chance to make a bad move
                return random.choice([1, 2, 9, 10])  # Extreme values
            return base_move
            
        elif difficulty == Difficulty.MEDIUM:
            # Medium mode - avoids obvious mistakes
            if is_batting:
                return base_move
            else:
                # When bowling, avoids player's last move
                if self.player_history and random.random() < 0.6:
                    return random.choice([x for x in range(MIN_SCORE, MAX_SCORE+1) 
                                      if x != self.player_history[-1]])
                return base_move
                
        elif difficulty == Difficulty.HARD:
            # Hard mode - uses advanced strategy
            if target is not None:
                needed = target - player_score if is_batting else player_score - target
                
                if is_batting:
                    if needed <= MAX_SCORE:
                        # Try to reach target exactly
                        return min(needed, MAX_SCORE)
                else:
                    if player_score + MAX_SCORE >= target:
                        # Try to prevent player from reaching target
                        return max(MIN_SCORE, (target - player_score) - 1)
            
            # Pattern recognition
            if len(self.player_history) >= 3:
                last_three = self.player_history[-3:]
                if len(set(last_three)) == 1:  # Player repeating same number
                    predicted = (last_three[0] + 1) % (MAX_SCORE + 1) or MAX_SCORE
                else:
                    predicted = max(set(last_three), key=last_three.count)
                
                # Add some randomness
                offset = random.choice([-1, 0, 1])
                return max(MIN_SCORE, min(MAX_SCORE, predicted + offset))
        
        return base_move

    def play_innings(self, batter: str, difficulty: Difficulty, target: Optional[int] = None) -> Tuple[int, bool]:
        score = 0
        is_player = batter == 'player'
        perfect = True
        
        print(self.color_text(f"\n{'» You are batting! «' if is_player else f'» {self.bot.name} is batting! «'}", 'highlight'))
        
        while True:
            if is_player:
                # Player batting (computer bowling)
                player_move = self.get_player_move()
                comp_move = self.get_computer_move(difficulty, is_batting=False, player_score=score, target=target)
                
                print(f"\n{self.color_text(f'{self.bot.name} bowled:', 'primary')} {self.color_text(comp_move, 'highlight')}")
                
                if player_move == comp_move:
                    print(self.color_text("\n» OUT! Innings over.", 'danger'))
                    print(f"{self.bot.name}: \"Got you!\"")
                    perfect = False
                    break
                    
                score += player_move
                print(f"{self.color_text('» Current score: ', 'primary')}{self.color_text(score, 'success')}")
                
                # Show progress when chasing target
                if target is not None:
                    needed = max(0, target - score)
                    print(f"{self.color_text('» Runs needed: ', 'primary')}{self.color_text(needed, 'warning' if needed > 0 else 'success')}")
                    print(f"Progress: {self.progress_bar(score, target)}")
                    
                    if score >= target:
                        break
            else:
                # Computer batting (player bowling)
                comp_move = self.get_computer_move(difficulty, is_batting=True, player_score=score, target=target)
                player_move = self.get_player_move()
                
                print(f"\n{self.color_text('You bowled:', 'primary')} {self.color_text(player_move, 'highlight')}")
                
                if comp_move == player_move:
                    print(self.color_text("\n» OUT! Innings over.", 'danger'))
                    perfect = False
                    break
                    
                score += comp_move
                print(f"{self.color_text('» Current score: ', 'primary')}{self.color_text(score, 'danger')}")
                
                # Show progress when defending target
                if target is not None:
                    ahead = max(0, score - target)
                    print(f"{self.color_text('» Runs ahead: ', 'primary')}{self.color_text(ahead, 'danger' if ahead > 0 else 'success')}")
                    print(f"Progress: {self.progress_bar(score, target)}")
                    
                    if score >= target:
                        break
        
        return score, perfect

    def update_stats(self, score: int, outcome: str, difficulty: Difficulty):
        """Updated to include difficulty in rank points calculation"""
        self.stats.games_played += 1
        self.stats.total_score += score
        
        if self.bot.name not in self.stats.rivalries:
            self.stats.rivalries[self.bot.name] = 0
        
        # XP is always earned, never deducted
        xp_gain = score * (20 if outcome == "win" else 10 if outcome == "tie" else 5)
        self.stats.xp += xp_gain
        
        # Rank points are affected by difficulty
        if outcome == "win":
            self.stats.wins += 1
            self.stats.rivalries[self.bot.name] += 1
            self.stats.streak += 1
            
            # Base RP + streak bonus + difficulty bonus
            base_rp = 20
            streak_bonus = 5 * min(self.stats.streak, 5)
            difficulty_bonus = {
                Difficulty.EASY: 5,
                Difficulty.MEDIUM: 10,
                Difficulty.HARD: 20
            }[difficulty]
            
            rank_points_gain = base_rp + streak_bonus + difficulty_bonus
            self.stats.rank_points += rank_points_gain
            
        elif outcome == "loss":
            self.stats.losses += 1
            self.stats.streak = 0
            
            # Smaller penalty based on difficulty
            rank_points_loss = {
                Difficulty.EASY: 5,
                Difficulty.MEDIUM: 10,
                Difficulty.HARD: 15
            }[difficulty]
            self.stats.rank_points = max(0, self.stats.rank_points - rank_points_loss)
            
        else:  # tie
            self.stats.ties += 1
            self.stats.streak = 0
            rank_points_gain = 5  # Small reward for ties
            self.stats.rank_points += rank_points_gain
        
        # Level up check
        xp_needed = int(BASE_XP * (self.stats.level ** XP_SCALING))
        while self.stats.xp >= xp_needed:
            self.stats.level += 1
            self.stats.xp -= xp_needed
            xp_needed = int(BASE_XP * (self.stats.level ** XP_SCALING))
            print(self.color_text(f"\n» LEVEL UP! You are now Level {self.stats.level}", 'success'))
        
        # Rank up/down check
        current_rank_index = RANKS.index(self.stats.rank)
        if current_rank_index < len(RANKS) - 1 and self.stats.rank_points >= 100:
            self.stats.rank = RANKS[current_rank_index + 1]
            self.stats.rank_points = 0
            print(self.color_text(f"\n» RANK UP! You are now a {self.stats.rank}!", 'highlight'))
        elif current_rank_index > 0 and self.stats.rank_points <= 0:
            self.stats.rank = RANKS[current_rank_index - 1]
            self.stats.rank_points = 50
            print(self.color_text(f"\n» RANK DOWN! You are now a {self.stats.rank}.", 'danger'))
        
        return xp_gain, self.stats.rank_points

    def check_achievements(self, score: int, difficulty: Difficulty, perfect: bool, was_behind: bool):
        if score >= 50 and self.achievements.unlock("50 Run Blitz"):
            print(self.color_text("\n» Achievement Unlocked: 50 Run Blitz! 🏅", 'success'))
        
        if score >= 100 and self.achievements.unlock("Centurion"):
            print(self.color_text("\n» Achievement Unlocked: Centurion! 🏅", 'success'))
        
        if self.stats.streak >= 3 and self.achievements.unlock("Hat-Trick Hero"):
            print(self.color_text("\n» Achievement Unlocked: Hat-Trick Hero! 🎩", 'success'))
        
        if difficulty == Difficulty.HARD and self.achievements.unlock("Hard Mode Champion"):
            print(self.color_text("\n» Achievement Unlocked: Hard Mode Champion! 💪", 'success'))
        
        if perfect and self.achievements.unlock("Flawless Victory"):
            print(self.color_text("\n» Achievement Unlocked: Flawless Victory! ✨", 'success'))
        
        if self.stats.games_played >= 10 and self.achievements.unlock("Veteran Player"):
            print(self.color_text("\n» Achievement Unlocked: Veteran Player! 🎖️", 'success'))
        
        if self.bot.name in self.stats.rivalries and self.stats.rivalries[self.bot.name] >= 3:
            if self.achievements.unlock("Rivalry Settled"):
                print(self.color_text(f"\n» Achievement Unlocked: Rivalry Settled (vs {self.bot.name})! ⚔️", 'success'))
        
        beaten_personalities = {
            bot_name: self.stats.rivalries.get(bot_name, 0) > 0
            for bot_name in ['Fankara', 'Lobamgi', 'Fola', 'Das', 'James', 'Rad']
        }
        if all(beaten_personalities.values()) and self.achievements.unlock("Style Master"):
            print(self.color_text("\n» Achievement Unlocked: Style Master! 🎭", 'success'))
        
        if was_behind and self.achievements.unlock("Comeback King"):
            print(self.color_text("\n» Achievement Unlocked: Comeback King! 👑", 'success'))

    def show_stats(self):
        self.print_header("Player Statistics")
        print(f"{self.color_text('Level:', 'primary')} {self.stats.level}")
        print(f"{self.color_text('XP:', 'primary')} {self.progress_bar(self.stats.xp, int(BASE_XP * (self.stats.level ** XP_SCALING)))}")
        print(f"{self.color_text('Rank:', 'primary')} {self.stats.rank} [{self.stats.rank_points}/100 RP]")
        print(f"{self.color_text('Wins:', 'success')} {self.stats.wins} {self.color_text('Losses:', 'danger')} {self.stats.losses} {self.color_text('Ties:', 'highlight')} {self.stats.ties}")
        print(f"{self.color_text('Win Streak:', 'highlight')} {self.stats.streak}")
        print(f"{self.color_text('High Score:', 'warning')} {self.stats.high_score}")
        print(f"{self.color_text('Total Runs:', 'primary')} {self.stats.total_score}")
        
        if self.stats.rivalries:
            print("\n" + self.color_text("Rivalries:", 'highlight'))
            for bot, wins in self.stats.rivalries.items():
                print(f"{bot}: {wins} {'win' if wins == 1 else 'wins'}")

    def play_match(self):
        self.print_header("New Match Starting!")
        print(f"Opponent: {self.bot.describe()}")
        time.sleep(1)
        
        difficulty = Difficulty(self.get_valid_input(
            "Choose difficulty (easy/medium/hard): ",
            [d.value for d in Difficulty]
        ))
        
        decision = self.simulate_toss()
        player_score, comp_score = 0, 0
        perfect_game = False
        was_behind = False

        if decision == GameMode.BAT:
            print(self.color_text("\n» You're batting first!", 'success'))
            player_score, _ = self.play_innings('player', difficulty)
            print(self.color_text(f"\n» Your innings total: {player_score}", 'success'))
            
            print(f"\n{self.bot.name}: \"{self.bot.get_taunt()}\"")
            time.sleep(1)
            
            print(self.color_text("\n» Now bowling to defend your score!", 'primary'))
            comp_score, _ = self.play_innings('computer', difficulty, player_score)
        else:
            print(self.color_text("\n» You're bowling first!", 'primary'))
            comp_score, _ = self.play_innings('computer', difficulty)
            print(self.color_text(f"\n» {self.bot.name}'s innings total: {comp_score}", 'danger'))
            
            if comp_score > 0:
                was_behind = True
                print(f"\n{self.bot.name}: \"{self.bot.get_taunt()}\"")
                time.sleep(1)
            
            print(self.color_text("\n» Now batting to chase the target!", 'success'))
            player_score, perfect_game = self.play_innings('player', difficulty, comp_score)

        self.print_header("Match Result")
        print(f"{self.color_text('Your Score:', 'success')} {player_score}")
        print(f"{self.color_text(f'{self.bot.name}\'s Score:', 'danger')} {comp_score}")
        
        if player_score > comp_score:
            print(self.color_text("\n» VICTORY! You won the match! 🎉", 'success'))
            print(f"{self.bot.name}: \"{self.bot.get_lose_phrase()}\"")
            xp, rp = self.update_stats(player_score, "win", difficulty)
            if perfect_game:
                print(self.color_text("» FLAWLESS VICTORY! You didn't get out!", 'highlight'))
        elif player_score < comp_score:
            print(self.color_text("\n» DEFEAT! Better luck next time! 💔", 'danger'))
            print(f"{self.bot.name}: \"{self.bot.get_win_phrase()}\"")
            xp, rp = self.update_stats(player_score, "loss", difficulty)
        else:
            print(self.color_text("\n» MATCH TIED! What a close game! 🤝", 'highlight'))
            print(f"{self.bot.name}: \"That was intense!\"")
            xp, rp = self.update_stats(player_score, "tie", difficulty)
        
        self.check_achievements(player_score, difficulty, perfect_game, was_behind)
        self.show_stats()
        self.save_game_data()

    def setup_game(self):
        self.print_header("Odd-Even Cricket Game")
        self.player_name = input(self.color_text("Enter your name: ", 'warning')).strip() or "Player"
        self.player_country = input(self.color_text("Enter your country: ", 'warning')).strip() or "Unknown"
        self.theme = self.get_valid_input("Choose theme (dark/light/neon): ", list(THEMES.keys()))
        self.bot = CricketBot()
        print(self.color_text(f"\n» {self.player_name} ({self.player_country}) vs {self.bot.name} ({self.bot.country})", 'highlight'))
        print(f"» {self.bot.describe()}")

    def main_menu(self):
        while True:
            self.print_header("Main Menu")
            print("1. Play Match")
            print("2. View Stats")
            print("3. Change Theme")
            print("4. New Opponent")
            print("5. Quit")
            
            choice = self.get_valid_input("Select an option: ", ['1', '2', '3', '4', '5'])
            
            if choice == '1':
                self.play_match()
            elif choice == '2':
                self.show_stats()
            elif choice == '3':
                self.theme = self.get_valid_input("Choose theme (dark/light/neon): ", list(THEMES.keys()))
            elif choice == '4':
                self.bot = CricketBot()
                print(self.color_text(f"\nNew opponent: {self.bot.describe()}", 'highlight'))
            else:
                print(self.color_text("\nThanks for playing! Goodbye! ✨", 'highlight'))
                break

if __name__ == "__main__":
    game = OddEvenGame()
    game.setup_game()
    game.main_menu()