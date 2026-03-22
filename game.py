"""
╔══════════════════════════════════════════╗
║   ROCK PAPER SCISSORS LIZARD SPOCK 🎮   ║
╚══════════════════════════════════════════╝

Concepts Covered:
- Functions & Return Values
- Dictionaries & Nested Dictionaries
- Loops (while, for)
- Conditionals (if/elif/else)
- Random Module
- File I/O (JSON for leaderboard)
- Classes & OOP
- Exception Handling
- String Formatting
"""

import random
import json
import os
import time

# ─────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────
CHOICES = ["rock", "paper", "scissors", "lizard", "spock"]

EMOJIS = {
    "rock":     "🪨",
    "paper":    "📄",
    "scissors": "✂️",
    "lizard":   "🦎",
    "spock":    "🖖",
}

# wins[A][B] = "A beats B because..."
RULES = {
    "scissors": {"paper": "Scissors ✂️  cuts Paper 📄",
                 "lizard": "Scissors ✂️  decapitates Lizard 🦎"},
    "paper":    {"rock": "Paper 📄 covers Rock 🪨",
                 "spock": "Paper 📄 disproves Spock 🖖"},
    "rock":     {"lizard": "Rock 🪨 crushes Lizard 🦎",
                 "scissors": "Rock 🪨 crushes Scissors ✂️"},
    "lizard":   {"spock": "Lizard 🦎 poisons Spock 🖖",
                 "paper": "Lizard 🦎 eats Paper 📄"},
    "spock":    {"scissors": "Spock 🖖 smashes Scissors ✂️",
                 "rock": "Spock 🖖 vaporizes Rock 🪨"},
}

LEADERBOARD_FILE = "leaderboard.json"


# ─────────────────────────────────────────
# CLASS: Player  (OOP concept)
# ─────────────────────────────────────────
class Player:
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def total_games(self):
        return self.wins + self.losses + self.ties

    def win_rate(self):
        if self.total_games() == 0:
            return 0.0
        return round((self.wins / self.total_games()) * 100, 1)

    def record(self):
        return f"W:{self.wins} L:{self.losses} T:{self.ties} | Win Rate: {self.win_rate()}%"


# ─────────────────────────────────────────
# CLASS: AIOpponent (Strategy + Randomness)
# ─────────────────────────────────────────
class AIOpponent:
    def __init__(self, difficulty="medium"):
        self.difficulty = difficulty

    def choose(self, human_last_choice=None):
        """
        easy   → pure random
        medium → 30% chance to counter human's last move
        hard   → 60% chance to counter human's last move
        """
        if self.difficulty == "easy" or human_last_choice is None:
            return random.choice(CHOICES)

        counter_chance = 0.3 if self.difficulty == "medium" else 0.6

        if random.random() < counter_chance:
            for move, victims in RULES.items():
                if human_last_choice in victims:
                    return move

        return random.choice(CHOICES)


# ─────────────────────────────────────────
# UTILITY FUNCTIONS
# ─────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def slow_print(text, delay=0.03):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def banner():
    print("\033[96m")
    print("╔══════════════════════════════════════════════╗")
    print("║   🪨  ROCK  PAPER  SCISSORS  LIZARD  SPOCK  ║")
    print("║              ✨ Ultimate Edition ✨           ║")
    print("╚══════════════════════════════════════════════╝")
    print("\033[0m")


def countdown():
    for word in ["Rock...", "Paper...", "Scissors..."]:
        print(f"\r  ✊ {word}", end="", flush=True)
        time.sleep(0.6)
    print("\r  🎲 SHOOT!          ")
    time.sleep(0.4)


def get_player_choice():
    """Input validation with a while loop."""
    print("\n  Your choices:")
    for i, choice in enumerate(CHOICES, 1):
        print(f"    [{i}] {EMOJIS[choice]}  {choice.capitalize()}")
    print("    [q] Quit")

    while True:
        raw = input("\n  Enter number or name: ").strip().lower()

        if raw == "q":
            return None

        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(CHOICES):
                return CHOICES[idx]

        matches = [c for c in CHOICES if c.startswith(raw)]
        if len(matches) == 1:
            return matches[0]

        print("  ❌ Invalid choice. Try again.")


def determine_winner(p1, p2):
    """Dictionary lookup instead of long if/elif chains."""
    if p1 == p2:
        return "tie", "It's a tie! 🤝"
    if p2 in RULES[p1]:
        return "p1", RULES[p1][p2]
    if p1 in RULES[p2]:
        return "p2", RULES[p2][p1]
    return "tie", "It's a tie! 🤝"


def display_round_result(player, ai_choice, human_choice, result, reason):
    print(f"\n  You played  : {EMOJIS[human_choice]} {human_choice.capitalize()}")
    print(f"  AI played   : {EMOJIS[ai_choice]}  {ai_choice.capitalize()}")
    print(f"\n  📖 {reason}")

    if result == "p1":
        print("\033[92m  🏆 YOU WIN this round!\033[0m")
        player.wins += 1
    elif result == "p2":
        print("\033[91m  💀 AI WINS this round!\033[0m")
        player.losses += 1
    else:
        print("\033[93m  🤝 TIE!\033[0m")
        player.ties += 1

    print(f"\n  📊 Score → {player.record()}")


# ─────────────────────────────────────────
# LEADERBOARD  (File I/O + JSON)
# ─────────────────────────────────────────

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return {}
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)


def save_leaderboard(player):
    board = load_leaderboard()
    board[player.name] = {
        "wins": player.wins,
        "losses": player.losses,
        "ties": player.ties,
        "win_rate": player.win_rate()
    }
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(board, f, indent=4)


def show_leaderboard():
    board = load_leaderboard()
    if not board:
        print("\n  📋 No records yet. Be the first!\n")
        return

    print("\n\033[96m  ╔══════════ 🏆 LEADERBOARD 🏆 ══════════╗\033[0m")
    sorted_players = sorted(board.items(), key=lambda x: x[1]["win_rate"], reverse=True)
    for rank, (name, stats) in enumerate(sorted_players, 1):
        medal = ["🥇", "🥈", "🥉"][rank - 1] if rank <= 3 else f" {rank}."
        print(f"  {medal}  {name:<15} W:{stats['wins']} L:{stats['losses']} T:{stats['ties']}  ({stats['win_rate']}%)")
    print("\033[96m  ╚═══════════════════════════════════════╝\033[0m\n")


# ─────────────────────────────────────────
# MAIN GAME LOOP
# ─────────────────────────────────────────

def choose_difficulty():
    print("\n  Select AI Difficulty:")
    print("    [1] 😴 Easy   (random AI)")
    print("    [2] 🤔 Medium (smart AI)")
    print("    [3] 😈 Hard   (very smart AI)")
    levels = {"1": "easy", "2": "medium", "3": "hard"}
    while True:
        choice = input("  Enter 1/2/3: ").strip()
        if choice in levels:
            return levels[choice]
        print("  ❌ Please enter 1, 2, or 3.")


def main():
    clear()
    banner()

    name = input("  Enter your name, champion: ").strip() or "Player1"
    player = Player(name)
    difficulty = choose_difficulty()
    ai = AIOpponent(difficulty)

    slow_print(f"\n  ⚔️  Welcome, {player.name}! Facing AI on [{difficulty.upper()}] mode.\n")

    rounds = 0
    last_human_choice = None

    while True:
        print("\n" + "─" * 48)
        print(f"  Round {rounds + 1}  |  {player.record()}")
        print("─" * 48)

        human_choice = get_player_choice()
        if human_choice is None:
            print(f"\n  👋 Thanks for playing, {player.name}!")
            break

        ai_choice = ai.choose(last_human_choice)
        countdown()

        result, reason = determine_winner(human_choice, ai_choice)
        display_round_result(player, ai_choice, human_choice, result, reason)

        last_human_choice = human_choice
        rounds += 1

        if rounds % 5 == 0:
            show_leaderboard()
            if input("  Continue playing? (y/n): ").strip().lower() != "y":
                break

    save_leaderboard(player)
    print(f"\n  🎮 Game Over! You played {rounds} rounds.")
    print(f"  📊 Final → {player.record()}")
    show_leaderboard()


# Entry point — __name__ guard concept
if __name__ == "__main__":
    main()