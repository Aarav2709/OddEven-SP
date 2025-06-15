

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
        this.createBackgroundParticles();
        this.setupScrollAnimations();
        this.initAudio();
        this.initializeUI();
    }

    initializeUI() {
        
        const startBtn = document.getElementById('start-game');
        const startTossBtn = document.getElementById('start-toss');
        
        if (startBtn) startBtn.style.display = 'none';
        if (startTossBtn) startTossBtn.style.display = 'inline-block';
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
        
        gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);
        
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
            } else if (e.key === 'Escape') {
                
                this.closeModal();
            }
        });

        
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('number-btn')) {
                this.selectNumber(parseInt(e.target.dataset.number));
            }
        });

        
        const startTossBtn = document.getElementById('start-toss');
        const startBtn = document.getElementById('start-game');
        const playTurnBtn = document.getElementById('play-turn');
        const resetStatsBtn = document.getElementById('reset-stats');

        
        const callHeadsBtn = document.getElementById('call-heads');
        const callTailsBtn = document.getElementById('call-tails');
        const chooseBatBtn = document.getElementById('choose-bat');
        const chooseBowlBtn = document.getElementById('choose-bowl');
        const proceedBtn = document.getElementById('proceed-after-toss');

        if (startTossBtn) startTossBtn.addEventListener('click', () => this.showToss());
        if (startBtn) startBtn.addEventListener('click', () => this.startGame());
        if (playTurnBtn) playTurnBtn.addEventListener('click', () => this.playTurn());
        if (resetStatsBtn) resetStatsBtn.addEventListener('click', () => this.resetStats());

        
        if (callHeadsBtn) callHeadsBtn.addEventListener('click', () => this.performToss('heads'));
        if (callTailsBtn) callTailsBtn.addEventListener('click', () => this.performToss('tails'));
        if (chooseBatBtn) chooseBatBtn.addEventListener('click', () => this.chooseBattingOrder('bat'));
        if (chooseBowlBtn) chooseBowlBtn.addEventListener('click', () => this.chooseBattingOrder('bowl'));
        if (proceedBtn) proceedBtn.addEventListener('click', () => this.proceedToGame());

        
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeModal();
            }
        });
    }

    createBackgroundParticles() {
        const particlesContainer = document.querySelector('.bg-particles');
        if (!particlesContainer) return;

        const particleCount = 50;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 20 + 's';
            particle.style.animationDuration = (15 + Math.random() * 10) + 's';
            
            particlesContainer.appendChild(particle);
        }
    }

    setupScrollAnimations() {
        const header = document.querySelector('.header');
        if (!header) return;

        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });

        
        const animateOnScroll = () => {
            const elements = document.querySelectorAll('[data-animate]');
            elements.forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.top < window.innerHeight * 0.8) {
                    el.classList.add('animate-fade-in');
                }
            });
        };

        window.addEventListener('scroll', animateOnScroll);
        animateOnScroll(); 
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
        
        
        this.playSound(800, 0.1);
        
        
        document.querySelectorAll('.number-btn').forEach(btn => {
            btn.classList.remove('selected');
        });
        
        const selectedBtn = document.querySelector(`[data-number="${number}"]`);
        selectedBtn.classList.add('selected');
        
        
        selectedBtn.style.transform = 'scale(1.2)';
        setTimeout(() => {
            selectedBtn.style.transform = '';
        }, 150);
        
        
        const playBtn = document.getElementById('play-turn');
        if (playBtn && this.isGameActive) {
            playBtn.disabled = false;
            playBtn.classList.remove('disabled');
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
            coin.classList.add(tossResult + '-result');
            
            
            this.showTossResult(playerCall, tossResult, playerWon);
        }, 2000);

        
        this.playCoinFlipSound();
    }

    playCoinFlipSound() {
        if (!this.audioContext) return;
        
        
        const frequencies = [800, 600, 400, 500, 700];
        frequencies.forEach((freq, index) => {
            setTimeout(() => {
                this.playSound(freq, 0.1, 'triangle');
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

        outcomeEl.textContent = `It's ${result.toUpperCase()}! You called ${playerCall.toUpperCase()}.`;

        if (playerWon) {
            winnerMessageEl.innerHTML = '<p class="font-bold" style="color: #00ff00;">🎉 You won the toss!</p>';
            choiceSelectionEl.style.display = 'block';
            botChoiceEl.style.display = 'none';
        } else {
            winnerMessageEl.innerHTML = '<p class="font-bold" style="color: #ff4444;">😞 Bot won the toss!</p>';
            choiceSelectionEl.style.display = 'none';
            botChoiceEl.style.display = 'block';
            
            
            const botChoice = Math.random() < 0.5 ? 'bat' : 'bowl';
            document.getElementById('bot-decision').textContent = botChoice;
            
            
            
            const playerMode = botChoice === 'bat' ? 'bowl' : 'bat';
            const modeRadio = document.querySelector(`input[name="mode"][value="${playerMode}"]`);
            if (modeRadio) {
                modeRadio.checked = true;
            }
            
            console.log(`Bot chose to: ${botChoice}`);
            console.log(`Player will: ${playerMode}`);
            console.log(`Radio button value set to: ${modeRadio?.value}`);
            
            
            document.getElementById('proceed-after-toss').style.display = 'inline-block';
            
            
            this.tossWinner = 'bot';
            this.gameMode = playerMode; 
        }

        
        if (playerWon) {
            this.playSound(523, 0.3); 
        } else {
            this.playSound(220, 0.3); 
        }
    }

    chooseBattingOrder(choice) {
        this.tossWinner = 'player';
        this.gameMode = choice;
        
        
        const modeRadio = document.querySelector(`input[name="mode"][value="${choice}"]`);
        if (modeRadio) {
            modeRadio.checked = true;
        }
        
        
        document.getElementById('choice-selection').style.display = 'none';
        
        
        const winnerMessageEl = document.getElementById('toss-winner-message');
        winnerMessageEl.innerHTML = `<p class="font-bold">You chose to ${choice.toUpperCase()} first!</p>`;
        
        
        winnerMessageEl.innerHTML += `<button id="proceed-after-toss-inline" class="btn btn-primary" style="margin-top: 1rem;">Continue to Game</button>`;
        
        
        document.getElementById('proceed-after-toss-inline').addEventListener('click', () => this.proceedToGame());
    }

    proceedToGame() {
        
        document.getElementById('toss-result').style.display = 'none';
        document.getElementById('game-setup').style.display = 'block';
        
        
        const startBtn = document.getElementById('start-game');
        if (startBtn) {
            startBtn.textContent = 'Start Match';
            startBtn.style.display = 'inline-block';
        }
        
        
        const startTossBtn = document.getElementById('start-toss');
        if (startTossBtn) {
            startTossBtn.style.display = 'none';
        }
    }

    async startGame() {
        const playerName = document.getElementById('player-name')?.value || 'Player';
        const difficulty = document.getElementById('difficulty')?.value || 'medium';
        const modeRadio = document.querySelector('input[name="mode"]:checked');
        const mode = modeRadio ? modeRadio.value : 'bat';

        try {
            const response = await fetch('/api/start_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    player_name: playerName,
                    difficulty: difficulty,
                    mode: mode
                })
            });

            const data = await response.json();
            
            if (data.success) {
                this.currentGame = data.game_state;
                this.isGameActive = true;
                this.updateGameUI();
                this.showMessage(data.message, 'success');
                
                
                this.showGameInterface();
            } else {
                this.showMessage('Failed to start game', 'error');
            }
        } catch (error) {
            console.error('Error starting game:', error);
            this.showMessage('Error starting game', 'error');
        }
    }

    async playTurn() {
        if (!this.selectedNumber || !this.isGameActive) {
            this.showMessage('Please select a number first!', 'warning');
            return;
        }

        try {
            const response = await fetch('/api/play_turn', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    number: this.selectedNumber
                })
            });

            const data = await response.json();
            
            if (data.success) {
                this.currentGame = data.game_state;
                this.updateGameUI();
                
                
                this.showTurnResult(data.turn_result);
                
                
                if (this.currentGame.game_over) {
                    this.isGameActive = false;
                    this.showGameOver(data.turn_result);
                    this.updateStats(data.stats);
                }
                
                
                this.selectedNumber = null;
                document.querySelectorAll('.number-btn').forEach(btn => {
                    btn.classList.remove('selected');
                });
                
                const playBtn = document.getElementById('play-turn');
                if (playBtn) {
                    playBtn.disabled = true;
                    playBtn.classList.add('disabled');
                }
                
            } else {
                this.showMessage(data.error || 'Turn failed', 'error');
            }
        } catch (error) {
            console.error('Error playing turn:', error);
            this.showMessage('Error playing turn', 'error');
        }
    }

    showGameInterface() {
        const setupSection = document.getElementById('game-setup');
        const gameSection = document.getElementById('game-interface');
        
        if (setupSection) setupSection.style.display = 'none';
        if (gameSection) gameSection.style.display = 'block';
    }

    updateGameUI() {
        if (!this.currentGame) return;

        
        const playerScore = document.getElementById('player-score');
        const botScore = document.getElementById('bot-score');
        
        if (playerScore) playerScore.textContent = this.currentGame.player_score;
        if (botScore) botScore.textContent = this.currentGame.bot_score;

        
        const gameStatus = document.getElementById('game-status');
        if (gameStatus) {
            const phase = this.currentGame.game_phase === 'first_innings' ? '1st Innings' : '2nd Innings';
            const turn = this.currentGame.current_turn === 'player' ? 'Your Turn' : 'Bot Turn';
            gameStatus.textContent = `${phase} - ${turn}`;
        }

        
        const botInfo = document.getElementById('bot-info');
        if (botInfo && this.currentGame.bot) {
            botInfo.innerHTML = `
                <strong>${this.currentGame.bot.name}</strong> from ${this.currentGame.bot.country}
                <br><small>${this.currentGame.bot.personality} style</small>
            `;
        }
    }

    showTurnResult(turnResult) {
        const resultDiv = document.getElementById('turn-result');
        if (!resultDiv) return;

        
        let resultClass = 'animate-slide-up';
        let resultColor = 'var(--primary-black)';
        
        if (turnResult.numbers_match) {
            resultClass += ' animate-pulse';
            resultColor = '#ff4444'; 
        } else if (turnResult.total >= 15) {
            resultColor = '#44ff44'; 
        }

        resultDiv.innerHTML = `
            <div class="card ${resultClass}" style="border-color: ${resultColor}; transition: all 0.3s ease;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div class="text-mono" style="font-size: 1.2rem;">
                        <strong>You: ${turnResult.player_number}</strong> | <strong>Bot: ${turnResult.bot_number}</strong>
                    </div>
                    <div class="text-mono" style="font-size: 1.5rem; font-weight: bold;">
                        Total: ${turnResult.total}
                    </div>
                </div>
                <p style="font-size: 1.1rem; font-weight: bold; margin-bottom: 0.5rem;">${turnResult.message}</p>
                ${turnResult.bot_message ? `<p style="font-style: italic; opacity: 0.8;">"${turnResult.bot_message}"</p>` : ''}
            </div>
        `;

        
        if (turnResult.numbers_match) {
            
            this.playSound(200, 0.8, 'sawtooth');
            
            document.body.style.animation = 'flash 0.5s ease-in-out';
            setTimeout(() => {
                document.body.style.animation = '';
            }, 500);
        } else if (turnResult.total >= 15) {
            
            this.playSound(1000, 0.3);
            this.playSound(1200, 0.2);
        } else {
            
            this.playSound(600, 0.2);
        }

        
        setTimeout(() => {
            if (resultDiv.innerHTML) {
                resultDiv.style.opacity = '0';
                setTimeout(() => {
                    resultDiv.innerHTML = '';
                    resultDiv.style.opacity = '1';
                }, 300);
            }
        }, 4000);
    }

    showGameOver(turnResult) {
        const modal = document.getElementById('game-over-modal');
        const title = document.getElementById('game-over-title');
        const message = document.getElementById('game-over-message');
        const finalScore = document.getElementById('final-score');

        if (modal && title && message && finalScore) {
            title.textContent = turnResult.final_message || 'Game Over';
            message.textContent = turnResult.bot_message || '';
            finalScore.innerHTML = `
                <div class="stats-grid">
                    <div class="stat-item">
                        <span class="stat-number">${this.currentGame.player_score}</span>
                        <span class="stat-label">Your Score</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">${this.currentGame.bot_score}</span>
                        <span class="stat-label">Bot Score</span>
                    </div>
                </div>
            `;
            
            modal.classList.add('active');
        }
    }

    async newGame() {
        try {
            await fetch('/api/reset_game', { method: 'POST' });
            
            this.currentGame = null;
            this.isGameActive = false;
            this.selectedNumber = null;
            this.tossWinner = null;
            this.gameMode = null;
            
            
            const setupSection = document.getElementById('game-setup');
            const gameSection = document.getElementById('game-interface');
            const tossInterface = document.getElementById('toss-interface');
            const tossResult = document.getElementById('toss-result');
            
            if (setupSection) setupSection.style.display = 'block';
            if (gameSection) gameSection.style.display = 'none';
            if (tossInterface) tossInterface.style.display = 'none';
            if (tossResult) tossResult.style.display = 'none';
            
            
            const coin = document.getElementById('coin');
            if (coin) {
                coin.classList.remove('flip', 'heads-result', 'tails-result');
            }
            
            
            const callHeadsBtn = document.getElementById('call-heads');
            const callTailsBtn = document.getElementById('call-tails');
            if (callHeadsBtn) callHeadsBtn.disabled = false;
            if (callTailsBtn) callTailsBtn.disabled = false;
            
            
            const startTossBtn = document.getElementById('start-toss');
            const startBtn = document.getElementById('start-game');
            if (startTossBtn) startTossBtn.style.display = 'inline-block';
            if (startBtn) startBtn.style.display = 'none';
            
            
            const resultDiv = document.getElementById('turn-result');
            if (resultDiv) resultDiv.innerHTML = '';
            
            this.closeModal();
            this.showMessage('Ready for a new game!', 'success');
            
        } catch (error) {
            console.error('Error resetting game:', error);
            this.showMessage('Error resetting game', 'error');
        }
    }

    async resetStats() {
        if (!confirm('Are you sure you want to reset all stats? This cannot be undone.')) {
            return;
        }

        try {
            const response = await fetch('/api/reset_stats', { method: 'POST' });
            const data = await response.json();
            
            if (data.success) {
                this.updateStats(data.stats);
                this.showMessage('Stats reset successfully!', 'success');
            }
        } catch (error) {
            console.error('Error resetting stats:', error);
            this.showMessage('Error resetting stats', 'error');
        }
    }

    updateStats(stats) {
        
        const statsElements = {
            'wins': stats.wins,
            'losses': stats.losses,
            'ties': stats.ties,
            'games-played': stats.games_played,
            'high-score': stats.high_score,
            'level': stats.level,
            'rank': stats.rank,
            'streak': stats.streak
        };

        Object.entries(statsElements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });

        
        const xpBar = document.getElementById('xp-progress');
        if (xpBar) {
            const xpForNextLevel = stats.level * 100;
            const currentXp = stats.xp % 100;
            const progress = (currentXp / 100) * 100;
            xpBar.style.width = progress + '%';
        }
    }

    showMessage(message, type = 'info') {
        
        return;
    }

    closeModal() {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => modal.classList.remove('active'));
    }
}


document.addEventListener('DOMContentLoaded', () => {
    window.game = new OddEvenGame();
});


function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function getWinRate(wins, total) {
    if (total === 0) return 0;
    return Math.round((wins / total) * 100);
}


if (typeof module !== 'undefined' && module.exports) {
    module.exports = OddEvenGame;
}
