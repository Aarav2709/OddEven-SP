from flask import Flask, render_template, request, jsonify, session
import random
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'oddeven-sp-secret-key-2025'

# Game constants
MAX_SCORE = 10
MIN_SCORE = 1
RANKS = [
    "Rookie", "Warrior", "Titan", "Blaster", "Striker", 
    "Smasher", "Dynamo", "Majestic", "Maverick", "Champion"
]

# Bot personalities and names
BOT_PERSONALITIES = {
    'aggressive': {
        'taunts': ["I'll smash you!", "Too easy!", "Boring!"],
        'compliments': ["Not bad.", "Lucky shot!", "Hmph!"],
        'win_phrases': ["I told you I'm the best!", "Better luck next time!"],
        'lose_phrases': ["You got lucky!", "I'll get you next time!"]
    },
    'defensive': {
        'taunts': ["You can't break me!", "I'm unbreakable!", "Try harder!"],
        'compliments': ["Good try.", "Nice move", "Interesting."],
        'win_phrases': ["Defense wins games!", "Solid victory!"],
        'lose_phrases': ["Close match.", "Almost had it!"]
    },
    'tricky': {
        'taunts': ["Can you read me?", "Guess what's coming!", "I'm unpredictable!"],
        'compliments': ["You guessed right!", "Good read!", "Hmm."],
        'win_phrases': ["Mind games win!", "Outplayed!"],
        'lose_phrases': ["You read me well.", "Next time will be different!"]
    }
}

BOT_NAMES = ['Fankara', 'Lobamgi', 'Fola', 'Das', 'James', 'Rad']
BOT_COUNTRIES = ['West Indies', 'India', 'Australia', 'England']

class GameBot:
    def __init__(self):
        self.name = random.choice(BOT_NAMES)
        self.country = random.choice(BOT_COUNTRIES)
        self.personality = random.choice(list(BOT_PERSONALITIES.keys()))
        
    def get_message(self, message_type):
        return random.choice(BOT_PERSONALITIES[self.personality][message_type])
    
    def get_number(self, difficulty='medium', player_history=None):
        """Smart bot number selection based on difficulty and player patterns"""
        if player_history is None:
            player_history = []
        
        if difficulty == 'easy':
            # Easy: More predictable patterns, limited range
            return random.randint(1, 6)
        elif difficulty == 'hard':
            # Hard: Try to predict player patterns
            if len(player_history) >= 3:
                # Look for patterns in last 3 moves
                recent_moves = player_history[-3:]
                # Avoid the most common recent number
                common_number = max(set(recent_moves), key=recent_moves.count)
                # Sometimes pick the same number to get player out
                if random.random() < 0.3:
                    return common_number
                else:
                    # Pick a different number
                    available = [i for i in range(1, 11) if i != common_number]
                    return random.choice(available)
            else:
                return random.randint(1, 10)
        else:
            # Medium: Balanced approach with some strategy
            if len(player_history) >= 2:
                last_number = player_history[-1]
                # 20% chance to pick same number as last player move
                if random.random() < 0.2:
                    return last_number
            return random.randint(1, 8)

def init_session():
    if 'stats' not in session:
        session['stats'] = {
            'wins': 0,
            'losses': 0,
            'ties': 0,
            'games_played': 0,
            'high_score': 0,
            'total_score': 0,
            'level': 1,
            'xp': 0,
            'rank': RANKS[0],
            'streak': 0
        }
    if 'current_game' not in session:
        session['current_game'] = None

@app.route('/')
def index():
    init_session()
    return render_template('index.html', stats=session['stats'])

@app.route('/game')
def game():
    init_session()
    return render_template('game.html', stats=session['stats'])

@app.route('/stats')
def stats():
    init_session()
    return render_template('stats.html', stats=session['stats'])

@app.route('/progress')
def progress():
    init_session()
    return render_template('progress.html', stats=session['stats'])

@app.route('/achievements')
def achievements():
    init_session()
    return render_template('achievements.html', stats=session['stats'])

@app.route('/api/start_game', methods=['POST'])
def start_game():
    init_session()
    data = request.json
    
    bot = GameBot()
    
    game_state = {
        'player_name': data.get('player_name', 'Player'),
        'difficulty': data.get('difficulty', 'medium'),
        'mode': data.get('mode', 'bat'),  # bat or bowl
        'player_score': 0,
        'bot_score': 0,
        'player_out': False,
        'bot_out': False,
        'current_turn': 'player' if data.get('mode') == 'bat' else 'bot',
        'game_phase': 'first_innings',
        'bot': {
            'name': bot.name,
            'country': bot.country,
            'personality': bot.personality
        },
        'history': [],
        'game_over': False,
        'winner': None
    }
    
    session['current_game'] = game_state
    session.permanent = True
    
    return jsonify({
        'success': True,
        'game_state': game_state,
        'message': f"Game started! You're facing {bot.name} from {bot.country}"
    })

@app.route('/api/play_turn', methods=['POST'])
def play_turn():
    if 'current_game' not in session or not session['current_game']:
        return jsonify({'error': 'No active game'}), 400
    
    data = request.json
    game = session['current_game']
    player_number = data.get('number')
    
    if not player_number or player_number < 1 or player_number > 10:
        return jsonify({'error': 'Invalid number'}), 400
    
    # Generate bot number with player history for smarter AI
    bot = GameBot()
    bot.personality = game['bot']['personality']
    
    # Extract player numbers from history for AI analysis
    player_numbers = [turn['player_number'] for turn in game['history']]
    bot_number = bot.get_number(game['difficulty'], player_numbers)
    
    # Check if numbers match (player gets out)
    numbers_match = player_number == bot_number
    total = player_number + bot_number
    is_odd = total % 2 == 1
    
    turn_result = {
        'player_number': player_number,
        'bot_number': bot_number,
        'total': total,
        'is_odd': is_odd,
        'numbers_match': numbers_match
    }
    
    # Update scores based on current turn
    if game['current_turn'] == 'player':
        if numbers_match:
            game['player_out'] = True
            turn_result['message'] = f"OUT! Both picked {player_number}!"
            turn_result['bot_message'] = bot.get_message('taunts')
        else:
            game['player_score'] += player_number  # Only add batter's number
            turn_result['message'] = f"Scored {player_number} runs!"
            if player_number > 6:
                turn_result['bot_message'] = bot.get_message('compliments')
    else:
        if numbers_match:
            game['bot_out'] = True
            turn_result['message'] = f"Bowled out! Both picked {player_number}!"
            turn_result['bot_message'] = bot.get_message('lose_phrases')
        else:
            game['bot_score'] += bot_number  # Only add batter's number (bot is batting)
            turn_result['message'] = f"Bot scored {bot_number} runs!"
            turn_result['bot_message'] = bot.get_message('taunts')
    
    game['history'].append(turn_result)
    
    # Check for innings change or game end
    if game['current_turn'] == 'player' and game['player_out']:
        if game['game_phase'] == 'first_innings':
            game['current_turn'] = 'bot'
            game['game_phase'] = 'second_innings'
            game['player_out'] = False
        else:
            game['game_over'] = True
    elif game['current_turn'] == 'bot' and game['bot_out']:
        if game['game_phase'] == 'first_innings':
            game['current_turn'] = 'player'
            game['game_phase'] = 'second_innings'
            game['bot_out'] = False
        else:
            game['game_over'] = True
    
    # Check for game end conditions
    if game['game_phase'] == 'second_innings':
        if game['mode'] == 'bat':
            # Player batted first, now bot is chasing
            if game['bot_score'] > game['player_score']:
                game['game_over'] = True
                game['winner'] = 'bot'
        else:
            # Bot batted first, now player is chasing
            if game['player_score'] > game['bot_score']:
                game['game_over'] = True
                game['winner'] = 'player'
    
    # Determine final winner if game is over
    if game['game_over'] and not game['winner']:
        if game['player_score'] > game['bot_score']:
            game['winner'] = 'player'
        elif game['bot_score'] > game['player_score']:
            game['winner'] = 'bot'
        else:
            game['winner'] = 'tie'
    
    # Update session stats if game is over
    if game['game_over']:
        stats = session['stats']
        stats['games_played'] += 1
        stats['total_score'] += game['player_score']
        
        if game['player_score'] > stats['high_score']:
            stats['high_score'] = game['player_score']
        
        if game['winner'] == 'player':
            stats['wins'] += 1
            stats['streak'] += 1
            turn_result['final_message'] = "🎉 You Won!"
            turn_result['bot_message'] = bot.get_message('lose_phrases')
        elif game['winner'] == 'bot':
            stats['losses'] += 1
            stats['streak'] = 0
            turn_result['final_message'] = "😞 You Lost!"
            turn_result['bot_message'] = bot.get_message('win_phrases')
        else:
            stats['ties'] += 1
            turn_result['final_message'] = "🤝 It's a Tie!"
            turn_result['bot_message'] = "Good game!"
        
        # Update XP and level
        xp_gained = 50 if game['winner'] == 'player' else 20
        stats['xp'] += xp_gained
        new_level = min(10, stats['xp'] // 100 + 1)
        if new_level > stats['level']:
            stats['level'] = new_level
            stats['rank'] = RANKS[min(new_level - 1, len(RANKS) - 1)]
        
        session['stats'] = stats
    
    session['current_game'] = game
    session.permanent = True
    
    return jsonify({
        'success': True,
        'turn_result': turn_result,
        'game_state': game,
        'stats': session['stats']
    })

@app.route('/api/reset_game', methods=['POST'])
def reset_game():
    session['current_game'] = None
    return jsonify({'success': True})

@app.route('/api/reset_stats', methods=['POST'])
def reset_stats():
    session['stats'] = {
        'wins': 0,
        'losses': 0,
        'ties': 0,
        'games_played': 0,
        'high_score': 0,
        'total_score': 0,
        'level': 1,
        'xp': 0,
        'rank': RANKS[0],
        'streak': 0
    }
    return jsonify({'success': True, 'stats': session['stats']})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)