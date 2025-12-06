
class OddEvenGame {
    constructor() {
        this.currentGame = null;
        this.selectedNumber = null;
        this.isGameActive = false;
        this.audioContext = null;
        this.tossWinner = null;
        this.gameMode = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupScrollAnimations();
        this.initAudio();
        this.initializeUI();
    }

    initializeUI() {
        const startBtn = document.getElementById('start-game');
        const startTossBtn = document.getElementById('start-toss');

        if (startBtn) startBtn.style.display = 'none';
        if (startTossBtn) startTossBtn.style.display = 'inline-flex';
    }

    initAudio() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.log('Web Audio API not supported');
        }
    }

    playSound(frequency, duration, type = 'sine') {
        if (!this.audioContext) return;

        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);

        oscillator.frequency.value = frequency;
        oscillator.type = type;

        gainNode.gain.setValueAtTime(0.05, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + duration);

        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + duration);
    }

    setupEventListeners() {
        document.addEventListener('DOMContentLoaded', () => {
            this.updateNavigation();
        });

        document.addEventListener('keydown', (e) => {
            if (e.key >= '1' && e.key <= '9') {
                const number = parseInt(e.key);
                if (this.isGameActive) {
                    this.selectNumber(number);
                }
            } else if (e.key === '0') {
                if (this.isGameActive) {
                    this.selectNumber(10);
                }
            } else if (e.key === 'Enter' || e.key === ' ') {
                if (this.selectedNumber && this.isGameActive) {
                    e.preventDefault();
                    this.playTurn();
                }
            }
        });

        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('num-btn')) {
                this.selectNumber(parseInt(e.target.dataset.number));
            }
        });

        const startTossBtn = document.getElementById('start-toss');
        const startBtn = document.getElementById('start-game');
        const playTurnBtn = document.getElementById('play-turn');

        const callHeadsBtn = document.getElementById('call-heads');
        const callTailsBtn = document.getElementById('call-tails');
        const chooseBatBtn = document.getElementById('choose-bat');
        const chooseBowlBtn = document.getElementById('choose-bowl');
        const proceedBtn = document.getElementById('proceed-after-toss');

        if (startTossBtn) startTossBtn.addEventListener('click', () => this.showToss());
        if (startBtn) startBtn.addEventListener('click', () => this.startGame());
        if (playTurnBtn) playTurnBtn.addEventListener('click', () => this.playTurn());

        if (callHeadsBtn) callHeadsBtn.addEventListener('click', () => this.performToss('heads'));
        if (callTailsBtn) callTailsBtn.addEventListener('click', () => this.performToss('tails'));
        if (chooseBatBtn) chooseBatBtn.addEventListener('click', () => this.chooseBattingOrder('bat'));
        if (chooseBowlBtn) chooseBowlBtn.addEventListener('click', () => this.chooseBattingOrder('bowl'));
        if (proceedBtn) proceedBtn.addEventListener('click', () => this.proceedToGame());
    }

    setupScrollAnimations() {
        const nav = document.querySelector('.nav-container');
        if (!nav) return;

        window.addEventListener('scroll', () => {
            if (window.scrollY > 20) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });
    }

    updateNavigation() {
        const currentPage = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link');

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === currentPage ||
                (currentPage === '/' && link.getAttribute('href') === '/')) {
                link.classList.add('active');
            }
        });
    }

    selectNumber(number) {
        this.selectedNumber = number;
        this.playSound(600, 0.05);

        document.querySelectorAll('.num-btn').forEach(btn => {
            btn.classList.remove('selected');
        });

        const selectedBtn = document.querySelector(`[data-number="${number}"]`);
        if (selectedBtn) {
            selectedBtn.classList.add('selected');
        }

        const playBtn = document.getElementById('play-turn');
        if (playBtn && this.isGameActive) {
            playBtn.disabled = false;
        }
    }

    showToss() {
        document.getElementById('game-setup').style.display = 'none';
        document.getElementById('toss-interface').style.display = 'block';
    }

    async performToss(playerCall) {
        document.getElementById('call-heads').disabled = true;
        document.getElementById('call-tails').disabled = true;

        const coin = document.getElementById('coin');
        coin.classList.add('flip');

        const tossResult = Math.random() < 0.5 ? 'heads' : 'tails';
        const playerWon = playerCall === tossResult;

        setTimeout(() => {
            coin.classList.remove('flip');
            coin.classList.add(tossResult + '-win');
            this.showTossResult(playerCall, tossResult, playerWon);
        }, 2000);

        this.playCoinFlipSound();
    }

    playCoinFlipSound() {
        if (!this.audioContext) return;
        const frequencies = [800, 600, 400, 500, 700];
        frequencies.forEach((freq, index) => {
            setTimeout(() => {
                this.playSound(freq, 0.05, 'triangle');
            }, index * 100);
        });
    }

    showTossResult(playerCall, result, playerWon) {
        document.getElementById('toss-interface').style.display = 'none';
        document.getElementById('toss-result').style.display = 'block';

        const outcomeEl = document.getElementById('toss-outcome');
        const winnerMessageEl = document.getElementById('toss-winner-message');
        const choiceSelectionEl = document.getElementById('choice-selection');
        const botChoiceEl = document.getElementById('bot-choice');

        outcomeEl.textContent = `It's ${result.toUpperCase()}`;

        if (playerWon) {
            winnerMessageEl.innerHTML = '<p class="text-primary font-bold">You won the toss</p>';
            choiceSelectionEl.style.display = 'block';
            botChoiceEl.style.display = 'none';
        } else {
            winnerMessageEl.innerHTML = '<p class="text-primary font-bold">Bot won the toss</p>';
            choiceSelectionEl.style.display = 'none';
            botChoiceEl.style.display = 'block';

            const botChoice = Math.random() < 0.5 ? 'bat' : 'bowl';
            document.getElementById('bot-decision').textContent = botChoice.toUpperCase();

            const playerMode = botChoice === 'bat' ? 'bowl' : 'bat';
            const modeInput = document.querySelector(`input[name="mode"]`);
            if (modeInput) modeInput.value = playerMode;

            document.getElementById('proceed-after-toss').style.display = 'inline-flex';
            this.tossWinner = 'bot';
            this.gameMode = playerMode;
        }

        if (playerWon) {
            this.playSound(523, 0.2);
        } else {
            this.playSound(220, 0.2);
        }
    }

    chooseBattingOrder(choice) {
        this.tossWinner = 'player';
        this.gameMode = choice;
        const modeInput = document.querySelector(`input[name="mode"]`);
        if (modeInput) modeInput.value = choice;
        this.proceedToGame();
    }

    proceedToGame() {
        document.getElementById('toss-result').style.display = 'none';
        this.startGame();
    }

    async startGame() {
        if (this.audioContext && this.audioContext.state === 'suspended') {
            this.audioContext.resume();
        }
        const difficulty = document.querySelector('input[name="difficulty"]:checked')?.value || 'medium';
        const mode = this.gameMode || 'bat';

        try {
            const response = await fetch('/api/start_game', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ difficulty, mode })
            });
            const data = await response.json();

            if (data.success) {
                this.currentGame = data.game_state;
                this.isGameActive = true;
                this.updateGameUI();

                document.getElementById('game-setup').style.display = 'none';
                document.getElementById('game-interface').style.display = 'block';
                document.getElementById('game-over').style.display = 'none';

                // Reset UI
                document.getElementById('move-history').innerHTML = '';
                document.getElementById('commentary').textContent = '';

                this.playSound(440, 0.3);
            }
        } catch (error) {
            console.error('Error starting game:', error);
        }
    }

    async playTurn() {
        if (!this.selectedNumber || !this.isGameActive) return;

        const playBtn = document.getElementById('play-turn');
        playBtn.disabled = true;

        try {
            const response = await fetch('/api/play_turn', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ number: this.selectedNumber })
            });
            const data = await response.json();

            if (data.success) {
                this.currentGame = data.game_state;
                this.updateGameUI();
                this.addHistoryItem(data.turn_result);

                // Reset selection
                this.selectedNumber = null;
                document.querySelectorAll('.num-btn').forEach(btn => btn.classList.remove('selected'));

                if (data.game_state.game_over) {
                    this.endGame(data.game_state);
                }
            }
        } catch (error) {
            console.error('Error playing turn:', error);
            playBtn.disabled = false;
        }
    }

    updateGameUI() {
        const state = this.currentGame;

        document.getElementById('player-score').textContent = state.player_score;
        document.getElementById('bot-score').textContent = state.bot_score;

        const targetEl = document.getElementById('target-score');
        if (state.target) {
            targetEl.textContent = state.target;
        } else {
            targetEl.textContent = '-';
        }

        const inningsText = state.game_phase === 'first_innings' ? '1st Innings' : '2nd Innings';
        const statusText = state.current_turn === 'player' ? 'You are Batting' : 'You are Bowling';

        document.getElementById('current-innings').textContent = inningsText;
        document.getElementById('batting-status').textContent = statusText;
    }

    addHistoryItem(result) {
        const historyContainer = document.getElementById('move-history');
        const item = document.createElement('div');
        item.className = 'log-entry fade-in';

        const playerMove = result.player_number;
        const botMove = result.bot_number;
        const outcome = result.message;
        const isOut = result.numbers_match;

        let outcomeText = '';
        if (isOut) {
            outcomeText = 'OUT!';
            this.playSound(150, 0.4, 'sawtooth');
        } else {
            outcomeText = `+${playerMove === botMove ? 0 : (this.currentGame.current_turn === 'player' ? playerMove : botMove)}`;
            this.playSound(600, 0.1);
        }

        item.innerHTML = `
            <span>You: ${playerMove} | Bot: ${botMove}</span>
            <span>${outcomeText}</span>
        `;

        historyContainer.insertBefore(item, historyContainer.firstChild);

        const commentary = document.getElementById('commentary');
        commentary.textContent = result.commentary || outcome;
        commentary.classList.remove('fade-in');
        void commentary.offsetWidth; // Trigger reflow
        commentary.classList.add('fade-in');
    }

    endGame(state) {
        this.isGameActive = false;
        setTimeout(() => {
            document.getElementById('game-interface').style.display = 'none';
            document.getElementById('game-over').style.display = 'block';

            const title = document.getElementById('game-result-title');
            const message = document.getElementById('game-result-message');

            if (state.winner === 'player') {
                title.textContent = 'Victory!';
                message.textContent = 'You defeated the AI opponent.';
                this.playSound(523, 0.1);
                setTimeout(() => this.playSound(659, 0.1), 100);
                setTimeout(() => this.playSound(784, 0.2), 200);
            } else if (state.winner === 'bot') {
                title.textContent = 'Defeat';
                message.textContent = 'Better luck next time.';
                this.playSound(300, 0.3, 'sawtooth');
            } else {
                title.textContent = 'Tie Game';
                message.textContent = 'What a match!';
            }

            document.getElementById('final-player-score').textContent = state.player_score;
            document.getElementById('final-bot-score').textContent = state.bot_score;
        }, 1000);
    }
}

// Initialize game
const game = new OddEvenGame();
