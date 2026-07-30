import random
from enum import Enum
from typing import Dict, Optional, Tuple

import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

GAME_VERSION = "4.0.1"

MIN_RUN = 1
MAX_RUN = 10

RANKS = [
    "Rookie", "Warrior", "Titan", "Blaster", "Striker",
    "Smasher", "Dynamo", "Majestic", "Maverick", "Champion"
]


class GameMode(Enum):
    BAT = "bat"
    BOWL = "bowl"


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


THEMES = {
    "dark": {
        "text": Fore.WHITE,
        "primary": Fore.CYAN,
        "success": Fore.GREEN,
        "warning": Fore.YELLOW,
        "danger": Fore.RED,
        "highlight": Fore.MAGENTA
    },
    "light": {
        "text": Fore.BLACK,
        "primary": Fore.BLUE,
        "success": Fore.GREEN,
        "warning": Fore.YELLOW,
        "danger": Fore.RED,
        "highlight": Fore.MAGENTA
    },
    "neon": {
        "text": Fore.LIGHTWHITE_EX,
        "primary": Fore.LIGHTCYAN_EX,
        "success": Fore.LIGHTGREEN_EX,
        "warning": Fore.LIGHTYELLOW_EX,
        "danger": Fore.LIGHTRED_EX,
        "highlight": Fore.LIGHTMAGENTA_EX
    },
    "sunset": {
        "text": Fore.LIGHTWHITE_EX,
        "primary": Fore.LIGHTRED_EX,
        "success": Fore.LIGHTGREEN_EX,
        "warning": Fore.LIGHTYELLOW_EX,
        "danger": Fore.RED,
        "highlight": Fore.LIGHTBLUE_EX
    }
}


class TerminalUI:
    def __init__(self):
        self.theme = "dark"

    def set_theme(self, theme: str):
        if theme in THEMES:
            self.theme = theme

    def color(self, text: str, style: str = "text") -> str:
        colour = THEMES[self.theme].get(style, THEMES[self.theme]["text"])
        return f"{colour}{text}{Style.RESET_ALL}"

    def title(self, text: str):
        print()
        print(self.color(text.upper(), "highlight"))
        print()

    def section(self, text: str):
        print()
        print(self.color(text.upper(), "primary"))

    def message(self, text: str, style: str = "text"):
        print(self.color(text, style))

    def input(self, prompt: str) -> str:
        return input(self.color(prompt, "warning")).strip()

    def header(self):
        print()
        print(self.color("ODD EVEN SP", "primary"))
        print(self.color(f"Version {GAME_VERSION}"))
        print()


class CricketBot:
    NAMES = ["Fankara", "Lobamgi", "Fola", "Das", "James", "Rad"]
    COUNTRIES = ["India", "Australia", "England", "West Indies"]

    PERSONALITIES = {
        "Aggressive": {
            "intro": "Power hitter"
        },
        "Defensive": {
            "intro": "Strong defense"
        },
        "Tricky": {
            "intro": "Unpredictable"
        }
    }

    def __init__(self):
        self.name = random.choice(self.NAMES)
        self.country = random.choice(self.COUNTRIES)
        self.personality = random.choice(list(self.PERSONALITIES))

    def describe(self) -> Dict[str, str]:
        return {
            "Name": self.name,
            "Nation": self.country,
            "Style": self.personality,
            "Speciality": self.PERSONALITIES[self.personality]["intro"]
        }

    def comment(self, result: str) -> str:
        comments = {
            "win": [
                "Good match.",
                "You played well.",
                "I will return stronger."
            ],
            "loss": [
                "That was easy.",
                "Better luck next time.",
                "You need more practice."
            ],
            "hit": [
                "Interesting move.",
                "Good shot.",
                "Nice prediction."
            ]
        }
        return random.choice(comments[result])


class PlayerProfile:
    def __init__(self):
        self.name = "Player"
        self.country = "Unknown"
        self.level = 1
        self.xp = 0
        self.rank = RANKS[0]
        self.rank_points = 0
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.total_runs = 0
        self.high_score = 0
        self.games = 0
        self.streak = 0
        self.rivalries = {}

    def record_game(self, score: int):
        self.games += 1
        self.total_runs += score
        self.high_score = max(self.high_score, score)

    def add_xp(self, amount: int):
        self.xp += amount
        needed = self.level * 100

        while self.xp >= needed:
            self.xp -= needed
            self.level += 1
            needed = self.level * 100

    def add_rank_points(self, amount: int):
        self.rank_points += amount
        current = RANKS.index(self.rank)

        if self.rank_points >= 100 and current < len(RANKS) - 1:
            self.rank_points -= 100
            self.rank = RANKS[current + 1]

    def profile(self):
        return {
            "Name": self.name,
            "Country": self.country,
            "Level": self.level,
            "Rank": self.rank,
            "XP": self.xp,
            "Rank Points": self.rank_points,
            "Wins": self.wins,
            "Losses": self.losses,
            "Ties": self.ties,
            "Games": self.games,
            "Highest Score": self.high_score,
            "Total Runs": self.total_runs
        }

class MatchEngine:
    def __init__(self, ui: TerminalUI, player: PlayerProfile, achievements):
        self.ui = ui
        self.player = player
        self.achievements = achievements
        self.bot = CricketBot()
        self.history = []

    def get_number(self) -> int:
        while True:
            try:
                value = int(self.ui.input("Choose a number between 1 and 10: "))

                if MIN_RUN <= value <= MAX_RUN:
                    self.history.append(value)
                    return value

            except ValueError:
                pass

            self.ui.message("Invalid input.", "danger")

    def choose_difficulty(self) -> Difficulty:
        self.ui.section("Difficulty")
        self.ui.message("1. Easy")
        self.ui.message("2. Medium")
        self.ui.message("3. Hard")

        choices = {
            "1": Difficulty.EASY,
            "2": Difficulty.MEDIUM,
            "3": Difficulty.HARD
        }

        while True:
            choice = self.ui.input("Select difficulty: ")

            if choice in choices:
                return choices[choice]

    def toss(self) -> GameMode:
        self.ui.section("Toss")

        choice = self.ui.input("Choose heads or tails: ").lower()
        result = random.choice(["heads", "tails"])

        self.ui.message(f"Coin result: {result}", "primary")

        if choice == result:
            self.ui.message("You won the toss.", "success")

            decision = self.ui.input("Choose bat or bowl: ").lower()

            return GameMode.BAT if decision == "bat" else GameMode.BOWL

        self.ui.message(f"{self.bot.name} won the toss.", "danger")

        bot_choice = random.choice([
            GameMode.BAT,
            GameMode.BOWL
        ])

        self.ui.message(
            f"{self.bot.name} decided to {bot_choice.value}.",
            "warning"
        )

        return bot_choice

    def computer_move(
        self,
        difficulty: Difficulty,
        target: Optional[int] = None,
        score: int = 0
    ) -> int:

        if difficulty == Difficulty.EASY:
            return random.randint(MIN_RUN, MAX_RUN)

        if difficulty == Difficulty.MEDIUM:
            if self.history:
                choices = [
                    x for x in range(MIN_RUN, MAX_RUN + 1)
                    if x != self.history[-1]
                ]
                return random.choice(choices)

            return random.randint(MIN_RUN, MAX_RUN)

        if difficulty == Difficulty.HARD:
            if len(self.history) >= 3:
                recent = self.history[-3:]
                predicted = max(set(recent), key=recent.count)

                return max(
                    MIN_RUN,
                    min(MAX_RUN, predicted + random.choice([-1, 0, 1]))
                )

            if target:
                remaining = target - score

                if remaining <= MAX_RUN:
                    return remaining

        return random.randint(MIN_RUN, MAX_RUN)

    def innings(
        self,
        player_batting: bool,
        difficulty: Difficulty,
        target: Optional[int] = None
    ) -> Tuple[int, bool]:

        score = 0
        flawless = True

        self.ui.section(
            "Your Innings" if player_batting else f"{self.bot.name}'s Innings"
        )

        while True:
            if player_batting:
                player_number = self.get_number()

                bot_number = self.computer_move(
                    difficulty,
                    target,
                    score
                )

                self.ui.message(
                    f"{self.bot.name} bowled {bot_number}",
                    "primary"
                )

                if player_number == bot_number:
                    self.ui.message("You are out.", "danger")
                    flawless = False
                    break

                score += player_number

                self.ui.message(
                    f"Runs scored: {score}",
                    "success"
                )

            else:
                bot_number = self.computer_move(
                    difficulty,
                    target,
                    score
                )

                player_number = self.get_number()

                self.ui.message(
                    f"You bowled {player_number}",
                    "primary"
                )

                if player_number == bot_number:
                    self.ui.message(
                        "Opponent is out.",
                        "success"
                    )
                    break

                score += bot_number

                self.ui.message(
                    f"{self.bot.name} score: {score}",
                    "warning"
                )

            if target and score >= target:
                break

        return score, flawless

    def start_match(self):
        self.bot = CricketBot()
        self.history.clear()

        self.ui.title("Match Setup")

        self.ui.message("Opponent Profile")

        for key, value in self.bot.describe().items():
            self.ui.message(f"{key}: {value}")

        difficulty = self.choose_difficulty()
        mode = self.toss()

        player_score = 0
        bot_score = 0
        flawless = False

        if mode == GameMode.BAT:
            player_score, flawless = self.innings(True, difficulty)

            self.ui.message(
                f"Your total: {player_score}",
                "success"
            )

            bot_score, _ = self.innings(
                False,
                difficulty,
                player_score + 1
            )

        else:
            bot_score, _ = self.innings(False, difficulty)

            self.ui.message(
                f"Target: {bot_score + 1}",
                "primary"
            )

            player_score, flawless = self.innings(
                True,
                difficulty,
                bot_score + 1
            )

        self.result(
            player_score,
            bot_score,
            difficulty,
            flawless
        )

    def result(
        self,
        player_score: int,
        bot_score: int,
        difficulty: Difficulty,
        flawless: bool
    ):
        self.ui.title("Match Result")

        self.ui.message(f"Player: {player_score}")
        self.ui.message(f"{self.bot.name}: {bot_score}")

        self.player.record_game(player_score)

        if player_score > bot_score:
            self.ui.message("Victory", "success")
            self.player.wins += 1
            self.player.streak += 1
            reward = 50

        elif player_score < bot_score:
            self.ui.message("Defeat", "danger")
            self.player.losses += 1
            self.player.streak = 0
            reward = 15

        else:
            self.ui.message("Match Drawn", "warning")
            self.player.ties += 1
            self.player.streak = 0
            reward = 30

        self.player.add_xp(reward)
        self.player.add_rank_points(reward // 2)

        self.ui.message(
            f"XP gained: {reward}",
            "highlight"
        )

        unlocked = self.achievements.check(
            self.player,
            player_score,
            difficulty,
            flawless
        )

        for achievement in unlocked:
            self.ui.message(
                f"Achievement unlocked: {achievement}",
                "success"
            )

class AchievementSystem:
    def __init__(self):
        self.achievements = {
            "First Victory": False,
            "Fifty Runs": False,
            "Century": False,
            "Three Win Streak": False,
            "Veteran": False,
            "Hard Mode Winner": False,
            "Flawless Match": False
        }

    def check(
        self,
        player: PlayerProfile,
        score: int,
        difficulty: Difficulty,
        flawless: bool
    ):
        unlocked = []

        conditions = {
            "First Victory": player.wins >= 1,
            "Fifty Runs": score >= 50,
            "Century": score >= 100,
            "Three Win Streak": player.streak >= 3,
            "Veteran": player.games >= 10,
            "Hard Mode Winner": difficulty == Difficulty.HARD and player.wins >= 1,
            "Flawless Match": flawless
        }

        for name, condition in conditions.items():
            if condition and not self.achievements[name]:
                self.achievements[name] = True
                unlocked.append(name)

        return unlocked


class OddEvenSP:
    def __init__(self):
        self.ui = TerminalUI()
        self.player = PlayerProfile()
        self.achievements = AchievementSystem()
        self.engine = MatchEngine(
            self.ui,
            self.player,
            self.achievements
        )

    def setup(self):
        self.ui.header()

        name = self.ui.input("Enter player name: ")
        country = self.ui.input("Enter country: ")

        if name:
            self.player.name = name

        if country:
            self.player.country = country

    def show_profile(self):
        self.ui.title("Player Profile")

        for key, value in self.player.profile().items():
            self.ui.message(f"{key}: {value}")

    def show_achievements(self):
        self.ui.title("Achievements")

        for name, status in self.achievements.achievements.items():
            state = "Unlocked" if status else "Locked"
            self.ui.message(f"{name}: {state}")

    def training_mode(self):
        self.ui.title("Training Mode")

        runs = 0

        for ball in range(1, 7):
            self.ui.message(f"Ball {ball}")

            shot = self.engine.get_number()
            bowler = random.randint(MIN_RUN, MAX_RUN)

            if shot == bowler:
                self.ui.message(
                    "Bowled in training.",
                    "danger"
                )
                break

            runs += shot

            self.ui.message(
                f"Runs: {runs}",
                "success"
            )

        self.ui.message(
            f"Training score: {runs}"
        )

    def change_theme(self):
        self.ui.title("Theme Settings")

        themes = list(THEMES.keys())

        for index, theme in enumerate(themes, 1):
            self.ui.message(
                f"{index}. {theme.capitalize()}"
            )

        choice = self.ui.input("Select theme: ")

        try:
            theme = themes[int(choice) - 1]

            self.ui.set_theme(theme)

            self.ui.message(
                "Theme updated.",
                "success"
            )

        except (ValueError, IndexError):
            self.ui.message(
                "Invalid selection.",
                "danger"
            )

    def scout_opponent(self):
        self.engine.bot = CricketBot()

        self.ui.title("Opponent Scout")

        for key, value in self.engine.bot.describe().items():
            self.ui.message(
                f"{key}: {value}"
            )

    def menu(self):
        while True:
            self.ui.title("Main Menu")

            options = [
                "Start Match",
                "Player Profile",
                "Achievements",
                "Training Mode",
                "Theme Settings",
                "Scout Opponent",
                "Exit"
            ]

            for index, option in enumerate(options, 1):
                self.ui.message(
                    f"{index}. {option}"
                )

            choice = self.ui.input(
                "Select option: "
            )

            if choice == "1":
                self.engine.start_match()

            elif choice == "2":
                self.show_profile()

            elif choice == "3":
                self.show_achievements()

            elif choice == "4":
                self.training_mode()

            elif choice == "5":
                self.change_theme()

            elif choice == "6":
                self.scout_opponent()

            elif choice == "7":
                self.ui.message(
                    "Thank you for playing OddEven SP.",
                    "highlight"
                )
                break

            else:
                self.ui.message(
                    "Invalid option.",
                    "danger"
                )


if __name__ == "__main__":
    game = OddEvenSP()
    game.setup()
    game.menu()
