import json
import random
import sys

# Constants for repeated values
BAT = 'bat'
BOWL = 'bowl'
DIFFICULTIES = ['easy', 'medium', 'hard']
ACHIEVEMENTS_FILE = "achievements.json"
STATS_FILE = "player_stats.json"

# Initialize player stats
player_stats = {
    "wins": 0,
    "losses": 0,
    "total_score": 0,
    "level": 1,
    "xp": 0,
    "rank_points": 0,
    "rank": "Warrior"
}

# Initialize achievements
achievements = {
    "Score 50 Runs in a Game": False,
    "Score 100 Runs in a Game": False,
    "Win 3 Games in a Row": False,
    "Win a Game on Hard": False,
    "Win Without Getting Out": False
}

# Track consecutive wins
consecutive_wins = 0

# Rank System
RANKS = [
    "Warrior", "Titan", "Blaster", "Striker", "Smasher", "Dynamo",
    "Majestic", "Maverick", "Mighty", "Crusher", "Champion"
]

# Dark/Light Mode Setup
def choose_mode():
    """Let the user choose between dark and light mode."""
    mode = input("Choose your mode: 'light' or 'dark' 🌞🌚: ").strip().lower()
    while mode not in ['light', 'dark']:
        mode = input("Invalid mode! Choose 'light' or 'dark' 🌞🌚: ").strip().lower()
    return mode

mode = choose_mode()

colors = {
    'dark': {'red': '\033[91m', 'green': '\033[92m', 'yellow': '\033[93m', 'blue': '\033[94m', 'magenta': '\033[95m', 'cyan': '\033[96m', 'reset': '\033[0m'},
    'light': {'red': '\033[31m', 'green': '\033[32m', 'yellow': '\033[33m', 'blue': '\033[34m', 'magenta': '\033[35m', 'cyan': '\033[36m', 'reset': '\033[0m'}
}
color_mode = colors['dark'] if mode == 'dark' else colors['light']

# Player and Bot Customization
player_name = input("Enter your name: 🧑‍🦱👩‍🦱 ").strip()
player_country = input("Enter your country: 🌍 ").strip()
bot_names = ['Fankara', 'Lobamgi', 'Fola', 'Das', 'James', 'Rad', 'Logan', 'Sean', 'Osama', 'Jake', 'Guptill']
bot_countries = ['West Indies', 'India', 'Australia', 'England', 'South Africa', 'New Zealand', 'Scotland', 'Netherlands', 'Pakistan']
bot_name = random.choice(bot_names)
bot_country = random.choice(bot_countries)

# Add some color to the text output
def colored(text, color):
    """Return colored text based on the selected mode."""
    return f"{color_mode.get(color, color_mode['reset'])}{text}{color_mode['reset']}"

def progress_bar(current, target, length=20):
    """Display a progress bar for the current score."""
    progress = min(int((current / target) * length), length)  # Prevent overflow
    percentage = min(int((current / target) * 100), 100)      # Cap percentage at 100
    color = 'green' if percentage >= 70 else 'yellow' if percentage >= 40 else 'red'
    bar = f"[{'█' * progress}{' ' * (length - progress)}] {percentage}%"
    return f"Progress: {colored(bar, color)}"

def toss():
    """Simulate a coin toss and let the player choose to bat or bowl."""
    print(colored("\nToss Time! Choose Heads or Tails 🍀", 'cyan'))
    choice = get_valid_input("Enter 'Heads' or 'Tails': 🪙", ['heads', 'tails'])
    result = random.choice(['heads', 'tails'])
    print(f"\n{colored(f'Toss Result: {result.capitalize()} 🎯', 'magenta')}")

    if choice == result:
        print(colored("\nYou won the toss! 🎉", 'green'))
        decision = get_valid_input("\nDo you want to Bat 🏏 or Bowl 🏆 first? (Enter 'Bat' or 'Bowl'): ", [BAT, BOWL])
        return decision
    else:
        print(colored("\nYou lost the toss! Opponent will bowl first. 🏏", 'red'))
        return BOWL

def player_turn():
    """Get the player's input for their turn."""
    while True:
        try:
            player_input = int(input("Enter a number between 1 and 10: "))
            if 1 <= player_input <= 10:
                return player_input
            else:
                print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input! Please enter an integer between 1 and 10.")

def get_computer_input(difficulty, player_input=None, user_score=None, computer_score=None, player_history=None):
    """Generate computer's input based on the selected difficulty level."""
    if difficulty == 'easy':
        return random.randint(1, 10)

    elif difficulty == 'medium':
        # Avoids picking the same number as the player
        computer_input = random.randint(1, 10)
        while computer_input == player_input:
            computer_input = random.randint(1, 10)
        return computer_input

    elif difficulty == 'hard':
        if not player_history:
            player_history = []

        if len(player_history) >= 3:
            predicted_input = max(set(player_history[-3:]), key=player_history[-3:].count)
        else:
            predicted_input = random.randint(1, 10)

        if computer_score < user_score:
            return random.choice([predicted_input, predicted_input + 1]) % 10 or 10
        else:
            return random.choice([predicted_input - 1, predicted_input]) % 10 or 10

    # Default fallback if something goes wrong
    return random.randint(1, 10)

def get_valid_input(prompt, valid_options):
    """Get valid input from the user."""
    while True:
        user_input = input(colored(prompt, 'yellow')).strip().lower()
        if user_input in valid_options:
            return user_input
        print(colored(f"Invalid choice! Please choose from: {', '.join(valid_options)}", 'red'))

def check_achievements(user_score, difficulty, won_without_getting_out):
    """Check and unlock achievements based on the game outcome."""
    global achievements, consecutive_wins

    # Check scoring achievements
    if user_score >= 50 and not achievements["Score 50 Runs in a Game"]:
        achievements["Score 50 Runs in a Game"] = True
        print(colored("Achievement Unlocked: Score 50 Runs in a Game! 🏅", 'green'))

    if user_score >= 100 and not achievements["Score 100 Runs in a Game"]:
        achievements["Score 100 Runs in a Game"] = True
        print(colored("Achievement Unlocked: Score 100 Runs in a Game! 🏅", 'green'))

    # Check consecutive wins achievement
    if consecutive_wins >= 3 and not achievements["Win 3 Games in a Row"]:
        achievements["Win 3 Games in a Row"] = True
        print(colored("Achievement Unlocked: Win 3 Games in a Row! 🏅", 'green'))

    # Check difficulty achievement
    if difficulty == 'hard' and not achievements["Win a Game on Hard"]:
        achievements["Win a Game on Hard"] = True
        print(colored("Achievement Unlocked: Win a Game on Hard! 🏅", 'green'))

    # Check special achievement
    if won_without_getting_out and not achievements["Win Without Getting Out"]:
        achievements["Win Without Getting Out"] = True
        print(colored("Achievement Unlocked: Win Without Getting Out! 🏅", 'green'))

    # Track and display current streak
    print(colored(f"Current Win Streak: {consecutive_wins} 🏅", 'cyan'))

def save_data():
    """Save achievements and player stats to files."""
    try:
        with open(ACHIEVEMENTS_FILE, "w") as file:
            json.dump(achievements, file)
        with open(STATS_FILE, "w") as file:
            json.dump(player_stats, file)
    except Exception as e:
        print(colored(f"Error saving data: {str(e)}", 'red'))

def load_data():
    """Load achievements and player stats from files."""
    global achievements, player_stats
    try:
        with open(ACHIEVEMENTS_FILE, "r") as file:
            achievements = json.load(file)
        with open(STATS_FILE, "r") as file:
            player_stats = json.load(file)
    except FileNotFoundError:
        print(colored("Data files not found. Starting fresh.", 'yellow'))
    except Exception as e:
        print(colored(f"Error loading data: {str(e)}", 'red'))

def update_level_and_xp(score):
    """Update player level and XP based on the score."""
    global player_stats
    xp_gained = score * 10  # XP is proportional to the score
    player_stats["xp"] += xp_gained
    xp_required = int(100 * (player_stats["level"] ** 1.5))  # XP required increases exponentially

    while player_stats["xp"] >= xp_required:
        player_stats["level"] += 1
        player_stats["xp"] -= xp_required
        xp_required = int(100 * (player_stats["level"] ** 1.5))
        print(colored(f"Level Up! You are now Level {player_stats['level']} 🎉", 'green'))

    # Return XP gained for display in match summary
    return xp_gained

def update_rank(outcome):
    """Update player rank based on the game outcome."""
    global player_stats
    rank_index = RANKS.index(player_stats["rank"])
    points_gained = 20 if outcome == "win" else -10  # Gain or lose points

    player_stats["rank_points"] += points_gained

    # Ensure rank points don't go negative
    if player_stats["rank_points"] < 0:
        player_stats["rank_points"] = 0

    # Check for rank promotion or demotion
    if rank_index < len(RANKS) - 1 and player_stats["rank_points"] >= 100:
        player_stats["rank"] = RANKS[rank_index + 1]
        player_stats["rank_points"] = 0
        print(colored(f"Rank Up! You are now a {player_stats['rank']} 🎉", 'green'))
    elif rank_index > 0 and player_stats["rank_points"] < 0:
        player_stats["rank"] = RANKS[rank_index - 1]
        player_stats["rank_points"] = 50
        print(colored(f"Rank Down! You are now a {player_stats['rank']} 💔", 'red'))

    # Return points gained for display in match summary
    return points_gained

def odd_even_game():
    """Main game logic for the Odd-Even Game."""
    global player_stats, consecutive_wins
    print(colored(
        f"\nWelcome to the Odd-Even Game! Player: {player_name} ({player_country}) vs {bot_name} ({bot_country}) 🏆",
        'blue'))
    print(colored("Rules: Choose a number between 1-10. Your runs will add up. If you lose, the computer will play. ⚽",
                  'yellow'))

    # Choose difficulty
    difficulty = get_valid_input("\nChoose difficulty level (easy/medium/hard): ⚡", DIFFICULTIES)

    user_score = 0
    computer_score = 0

    user_decision = toss()  # Player decides whether to bat or bowl
    won_without_getting_out = False

    # Game logic based on whether the player decides to bat or bowl
    if user_decision == BAT:
        print(colored("\nYou are batting! 🏏", 'green'))
        while True:  # Infinite loop until someone gets out
            player_input = player_turn()
            computer_input = get_computer_input(difficulty, player_input, user_score, computer_score)
            print(f"\n{bot_name} chose: {colored(computer_input, 'cyan')} 🤖")
            if player_input == computer_input:
                print(colored("\nOut! Your innings is over. 🛑", 'red'))
                target_score = user_score
                won_without_getting_out = False
                break
            user_score += player_input
            print(f"Your current score: {colored(user_score, 'green')} 🏆\n")

        print(colored("\nYour opponent is batting now! 🏏", 'magenta'))
        while True:  # Infinite loop until someone gets out
            computer_input = get_computer_input(difficulty, user_score=user_score, computer_score=computer_score)
            player_input = player_turn()
            print(f"\n{bot_name} chose: {colored(computer_input, 'cyan')} 🤖")
            if player_input == computer_input:
                print(colored("\nComputer is out! You won the game! 🎉", 'green'))
                player_stats["wins"] += 1
                player_stats["total_score"] += user_score
                consecutive_wins += 1  # Increase streak
                xp_gained = update_level_and_xp(user_score)
                rp_gained = update_rank("win")
                break
            computer_score += computer_input
            print(f"Computer's current score: {colored(computer_score, 'red')} ⚡\n")

            # Now display progress bar only in second inning
            print(progress_bar(computer_score, user_score))  # Update progress bar

            if computer_score > user_score:
                print(colored("\nComputer has surpassed your score! Computer wins. 💥", 'red'))
                player_stats["losses"] += 1
                consecutive_wins = 0  # Reset streak
                xp_gained = update_level_and_xp(user_score)
                rp_gained = update_rank("loss")
                break

        if computer_score <= user_score:
            print(colored("\nCongratulations! You won the game. 🎉", 'green'))
    else:
        print(colored("\nComputer is batting first! 🏏", 'magenta'))
        while True:  # Infinite loop until someone gets out
            computer_input = get_computer_input(difficulty, user_score=user_score, computer_score=computer_score)
            player_input = player_turn()
            print(f"\n{bot_name} chose: {colored(computer_input, 'cyan')} 🤖")
            if player_input == computer_input:
                print(colored("\nComputer is out! Their innings is over. 🛑", 'red'))
                target_score = computer_score
                break
            computer_score += computer_input
            print(f"Computer's current score: {colored(computer_score, 'red')} ⚡\n")

        print(colored("\nYour turn to bat! 🏏", 'green'))
        while True:  # Infinite loop until someone gets out
            player_input = player_turn()
            computer_input = get_computer_input(difficulty, user_score=user_score, computer_score=computer_score)
            print(f"\n{bot_name} chose: {colored(computer_input, 'cyan')} 🤖")
            if player_input == computer_input:
                print(colored("\nOut! Your innings is over. 🛑", 'red'))
                won_without_getting_out = False
                break
            user_score += player_input
            print(f"Your current score: {colored(user_score, 'green')} 🏆\n")

            # Now display progress bar only in second inning
            print(progress_bar(user_score, computer_score))  # Update progress bar

            if user_score > computer_score:
                print(colored("\nYou have surpassed the computer's score! You win. 🎉", 'green'))
                player_stats["wins"] += 1
                player_stats["total_score"] += user_score
                consecutive_wins += 1  # Increase streak
                xp_gained = update_level_and_xp(user_score)
                rp_gained = update_rank("win")
                break

        if user_score <= computer_score:
            print(colored("\nComputer wins the game! Better luck next time. 💔", 'red'))
            player_stats["losses"] += 1
            consecutive_wins = 0  # Reset streak
            xp_gained = update_level_and_xp(user_score)
            rp_gained = update_rank("loss")

    # Match Summary with added emphasis
    print(colored("\n--- Match Summary --- 📜", 'blue'))
    print(f"Difficulty Level: {colored(difficulty.capitalize(), 'yellow')} ⚡")
    print(f"Your Final Score: {colored(user_score, 'green')} 🏆")
    print(f"{bot_name}'s Final Score: {colored(computer_score, 'red')} ⚡")

    if user_score > computer_score:
        print(colored("\nYou won the match! 🎉", 'green'))
    else:
        print(colored("\nComputer won the match! 💔", 'red'))

    # Display current stats in the desired format
    xp_required = int(100 * (player_stats["level"] ** 1.5))
    print(colored("\nYour Player Stats:", 'cyan'))
    print(f"Level: {player_stats['level']} [{player_stats['xp']}/{xp_required} XP] +{xp_gained} XP")
    print(f"Rank: {player_stats['rank']} [{player_stats['rank_points']}/100 RP] +{rp_gained} RP")
    print(f"Wins: {colored(player_stats['wins'], 'green')} 🏆")
    print(f"Losses: {colored(player_stats['losses'], 'red')} ⚡")
    print(f"Total Score: {colored(player_stats['total_score'], 'yellow')} 💯\n")

    check_achievements(user_score, difficulty, won_without_getting_out)
    save_data()

if __name__ == "__main__":
    load_data()
    while True:
        odd_even_game()
        play_again = input(colored("\nDo you want to play again? (yes/no): 🌟", 'yellow')).strip().lower()
        if play_again != 'yes':
            print(colored("\nThanks for playing! Goodbye! ✌️", 'magenta'))
            sys.exit()