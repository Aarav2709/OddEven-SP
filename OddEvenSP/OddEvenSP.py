import json
import random
import sys

# Initialize player stats
player_stats = {
    "wins": 0,
    "losses": 0,
    "total_score": 0
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

# Dark/Light Mode Setup
mode = input("Choose your mode: 'light' or 'dark' 🌞🌚: ").strip().lower()
while mode not in ['light', 'dark']:
    mode = input("Invalid mode! Choose 'light' or 'dark' 🌞🌚: ").strip().lower()

colors = {
    'dark': {'red': '\033[91m', 'green': '\033[92m', 'yellow': '\033[93m', 'blue': '\033[94m', 'magenta': '\033[95m', 'cyan': '\033[96m', 'reset': '\033[0m'},
    'light': {'red': '\033[31m', 'green': '\033[32m', 'yellow': '\033[33m', 'blue': '\033[34m', 'magenta': '\033[35m', 'cyan': '\033[36m', 'reset': '\033[0m'}
}
color_mode = colors['dark'] if mode == 'dark' else colors['light']

# Player and Bot Customization
player_name = input("Enter your name: 🧑‍🦱👩‍🦱 ").strip()
player_country = input("Enter your country: 🌍 ").strip()
bot_names = ['BotScorer 🤖', 'ScoreAI 🤖', 'IMBOT 🤖', 'NubBot 🤖']
bot_countries = ['USA 🇺🇸', 'India 🇮🇳', 'Australia 🇦🇺', 'England 🇬🇧']
bot_name = random.choice(bot_names)
bot_country = random.choice(bot_countries)

# Add some color to the text output
def colored(text, color):
    return f"{color_mode.get(color, color_mode['reset'])}{text}{color_mode['reset']}"

def progress_bar(current, target, length=20):
    """Generate a smooth progress bar based on score with color and animation."""
    progress = int((current / target) * length)  # Calculate the number of blocks to show
    percentage = int((current / target) * 100)  # Calculate percentage
    if percentage < 40:
        color = 'red'
    elif percentage < 70:
        color = 'yellow'
    else:
        color = 'green'

    bar = f"[{'█' * progress}{' ' * (length - progress)}] {percentage}%"
    return f"Progress: {colored(bar, color)}"

def toss():
    print(colored("\nToss Time! Choose Heads or Tails 🍀", 'cyan'))
    choice = input(colored("Enter 'Heads' or 'Tails': 🪙", 'yellow')).strip().lower()
    result = random.choice(['heads', 'tails'])
    print(f"\n{colored(f'Toss Result: {result.capitalize()} 🎯', 'magenta')}")
    if choice == result:
        print(colored("\nYou won the toss! 🎉", 'green'))
        decision = input(
            colored("\nDo you want to Bat 🏏 or Bowl 🏆 first? (Enter 'Bat' or 'Bowl'): ", 'yellow')).strip().lower()
        while decision not in ['bat', 'bowl']:
            print(colored("Invalid choice! Please enter 'Bat' or 'Bowl'.", 'red'))
            decision = input(
                colored("\nDo you want to Bat 🏏 or Bowl 🏆 first? (Enter 'Bat' or 'Bowl'): ", 'yellow')).strip().lower()
        return decision
    else:
        print(colored("\nYou lost the toss! Opponent will bowl first. 🏏", 'red'))
        return 'bowl'

def player_turn():
    # This function will get the player's input
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
    """
    Generate computer's input based on the selected difficulty level.
    """
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

def check_achievements(user_score, difficulty, won_without_getting_out):
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

def save_achievements():
    with open("achievements.json", "w") as file:
        json.dump(achievements, file)

def load_achievements():
    global achievements
    try:
        with open("achievements.json", "r") as file:
            achievements = json.load(file)
    except FileNotFoundError:
        pass

def odd_even_game():
    global player_stats, consecutive_wins
    print(colored(
        f"\nWelcome to the Odd-Even Game! Player: {player_name} ({player_country}) vs {bot_name} ({bot_country}) 🏆",
        'blue'))
    print(colored("Rules: Choose a number between 1-10. Your runs will add up. If you lose, the computer will play. ⚽",
                  'yellow'))

    # Choose difficulty
    difficulty = input(colored("\nChoose difficulty level (easy/medium/hard): ⚡", 'yellow')).strip().lower()
    while difficulty not in ['easy', 'medium', 'hard']:
        print(colored("Invalid difficulty level. Please choose 'easy', 'medium', or 'hard'. 🚫", 'red'))
        difficulty = input(colored("\nChoose difficulty level (easy/medium/hard): ⚡", 'yellow')).strip().lower()

    user_score = 0
    computer_score = 0

    user_decision = toss()  # Player decides whether to bat or bowl
    won_without_getting_out = False

    # Game logic based on whether the player decides to bat or bowl
    if user_decision == 'bat':
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
                break
            computer_score += computer_input
            print(f"Computer's current score: {colored(computer_score, 'red')} ⚡\n")

            # Now display progress bar only in second inning
            print(progress_bar(computer_score, user_score))  # Update progress bar

            if computer_score > user_score:
                print(colored("\nComputer has surpassed your score! Computer wins. 💥", 'red'))
                player_stats["losses"] += 1
                consecutive_wins = 0  # Reset streak
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
                break

        if user_score <= computer_score:
            print(colored("\nComputer wins the game! Better luck next time. 💔", 'red'))
            player_stats["losses"] += 1
            consecutive_wins = 0  # Reset streak

    # Match Summary with added emphasis
    print(colored("\n--- Match Summary --- 📜", 'blue'))
    print(f"Difficulty Level: {colored(difficulty.capitalize(), 'yellow')} ⚡")
    print(f"Your Final Score: {colored(user_score, 'green')} 🏆")
    print(f"{bot_name}'s Final Score: {colored(computer_score, 'red')} ⚡")

    if user_score > computer_score:
        print(colored("\nYou won the match! 🎉", 'green'))
    else:
        print(colored("\nComputer won the match! 💔", 'red'))

    print(colored("\nYour Player Stats:", 'cyan'))
    print(f"Wins: {colored(player_stats['wins'], 'green')} 🏆")
    print(f"Losses: {colored(player_stats['losses'], 'red')} ⚡")
    print(f"Total Score: {colored(player_stats['total_score'], 'yellow')} 💯\n")

    check_achievements(user_score, difficulty, won_without_getting_out)
    save_achievements()

if __name__ == "__main__":
    load_achievements()
    while True:
        odd_even_game()
        play_again = input(colored("\nDo you want to play again? (yes/no): 🌟", 'yellow')).strip().lower()
        if play_again != 'yes':
            print(colored("\nThanks for playing! Goodbye! ✌️", 'magenta'))
            sys.exit()
