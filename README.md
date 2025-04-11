So, welcome to my first ever **Python Project**! That is a game based on *Odd Even*, but with a twist of **Cricket!**
To install the Game, run `pip install OddEven-SP` in your Terminal. If you have already installed the game, then please run `pip install OddEven-SP --upgrade`. 

To initiate the game, you need to create a new Python File and type:
```py
from OddEvenSP import odd_even_game
odd_even_game()
```
# Enjoy! Make sure to give Feedback!

[![PyPI Downloads](https://static.pepy.tech/badge/oddeven-sp)](https://pepy.tech/projects/oddeven-sp)

# 🟡 OddEvenSP

OddEvenSP is a fun, interactive terminal-based game where you challenge a computer opponent in a thrilling game of odd-even cricket! Featuring dark/light mode, rank progression, achievements, and smart AI.

---

## 🚀 Installation

To install the game, just use pip:

```bash
pip install OddEvenSP
```

---

## ▶️ How to Play

Once installed, create a new Python file (e.g., `play.py`) and add the following:

```python
from OddEvenSP import main

main()
```

Then run it with:

```bash
python play.py
```

---

## 🎮 Features

- ✅ Difficulty Levels: Easy, Medium, Hard
- 🌑 Dark & Light Terminal Modes
- 🏆 Achievements & Stats System
- 🧠 Smart AI Opponent
- 📈 Rank & XP Progression System
- 📝 Data Saved Between Sessions (stats & achievements)
- 🎨 Colorful, fun CLI UI

---

## 📊 Player Stats & Achievements

Track your wins, losses, level, XP, rank, and unlock fun achievements like:

- "Score 50 Runs in a Game"
- "Win 3 Games in a Row"
- "Win Without Getting Out"

---

## ⚙️ Project Structure

```text
OddEvenSP/
├── __init__.py
├── main.py
├── achievements.json      # Stored achievements
├── player_stats.json      # Stored player stats
```

---

## 🧠 How the Game Works

- You pick a number between 1 and 10.
- So does the computer.
- If the numbers match → You're out!
- Score runs, beat the bot’s total, level up and rank up.

---

## 💡 Tip

Choose your mode wisely — the terminal theme affects how the colors appear.

---

## ❓ Support

Have questions or suggestions? Feel free to open an issue or start a discussion on the [GitHub repo](https://github.com/your-username/OddEvenSP).

---

## 📜 License

MIT License – use it, share it, improve it. 🚀

