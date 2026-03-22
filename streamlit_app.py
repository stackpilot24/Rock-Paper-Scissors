"""
🎮 Rock Paper Scissors - Streamlit Web UI
Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import random
import json
import os

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="RPS Ultimate",
    page_icon="🪨",
    layout="centered"
)

# ─────────────────────────────────────────
# CUSTOM CSS — dark neon theme
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background-color: #0a0a0f;
    color: #e0e0ff;
}

.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #0d0d20 100%);
}

h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
    color: #00ffcc !important;
    text-shadow: 0 0 20px #00ffcc88;
}

.title-glow {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 900;
    color: #00ffcc;
    text-shadow: 0 0 30px #00ffcc, 0 0 60px #00ffcc44;
    text-align: center;
    padding: 1rem 0;
    letter-spacing: 2px;
}

.choice-card {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid #00ffcc33;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    font-size: 3rem;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 4px 20px #00000066;
}

.choice-card:hover {
    border-color: #00ffcc;
    box-shadow: 0 0 20px #00ffcc44;
    transform: translateY(-4px);
}

.result-win {
    background: linear-gradient(135deg, #003322, #004433);
    border: 2px solid #00ff88;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    font-family: 'Orbitron', monospace;
    font-size: 1.5rem;
    color: #00ff88;
    text-shadow: 0 0 15px #00ff88;
    margin: 1rem 0;
}

.result-lose {
    background: linear-gradient(135deg, #330011, #440022);
    border: 2px solid #ff0055;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    font-family: 'Orbitron', monospace;
    font-size: 1.5rem;
    color: #ff0055;
    text-shadow: 0 0 15px #ff0055;
    margin: 1rem 0;
}

.result-tie {
    background: linear-gradient(135deg, #1a1a00, #2a2a00);
    border: 2px solid #ffcc00;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    font-family: 'Orbitron', monospace;
    font-size: 1.5rem;
    color: #ffcc00;
    text-shadow: 0 0 15px #ffcc00;
    margin: 1rem 0;
}

.score-box {
    background: #1a1a2e;
    border: 1px solid #00ffcc44;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}

.stButton > button {
    background: linear-gradient(135deg, #00ffcc22, #00ffcc11) !important;
    border: 1px solid #00ffcc !important;
    color: #00ffcc !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1.1rem !important;
    padding: 0.6rem 1.2rem !important;
    border-radius: 8px !important;
    transition: all 0.3s !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #00ffcc44, #00ffcc22) !important;
    box-shadow: 0 0 15px #00ffcc66 !important;
    transform: translateY(-2px) !important;
}

.leaderboard-row {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 1rem;
    border-bottom: 1px solid #ffffff11;
    font-family: 'Rajdhani', sans-serif;
}

div[data-testid="stSelectbox"] label {
    color: #00ffcc !important;
    font-family: 'Orbitron', monospace;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# GAME CONSTANTS
# ─────────────────────────────────────────
CHOICES = ["rock", "paper", "scissors", "lizard", "spock"]
EMOJIS = {"rock": "🪨", "paper": "📄", "scissors": "✂️", "lizard": "🦎", "spock": "🖖"}

RULES = {
    "scissors": {"paper": "Scissors cuts Paper",    "lizard": "Scissors decapitates Lizard"},
    "paper":    {"rock":  "Paper covers Rock",      "spock":  "Paper disproves Spock"},
    "rock":     {"lizard":"Rock crushes Lizard",    "scissors":"Rock crushes Scissors"},
    "lizard":   {"spock": "Lizard poisons Spock",   "paper":  "Lizard eats Paper"},
    "spock":    {"scissors":"Spock smashes Scissors","rock":  "Spock vaporizes Rock"},
}

LEADERBOARD_FILE = "leaderboard.json"


# ─────────────────────────────────────────
# SESSION STATE INIT  (Streamlit concept)
# ─────────────────────────────────────────
def init_state():
    defaults = {
        "wins": 0, "losses": 0, "ties": 0,
        "last_human": None, "last_ai": None,
        "last_result": None, "last_reason": "",
        "player_name": "Champion",
        "difficulty": "medium",
        "round": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────
# GAME LOGIC
# ─────────────────────────────────────────
def ai_choose(difficulty, last_human):
    if difficulty == "easy" or last_human is None:
        return random.choice(CHOICES)
    chance = 0.3 if difficulty == "medium" else 0.65
    if random.random() < chance:
        for move, victims in RULES.items():
            if last_human in victims:
                return move
    return random.choice(CHOICES)


def determine_winner(p1, p2):
    if p1 == p2:
        return "tie", "It's a tie!"
    if p2 in RULES[p1]:
        return "p1", RULES[p1][p2]
    if p1 in RULES[p2]:
        return "p2", RULES[p2][p1]
    return "tie", "It's a tie!"


def play_round(human_choice):
    ai_choice = ai_choose(st.session_state.difficulty, st.session_state.last_human)
    result, reason = determine_winner(human_choice, ai_choice)

    st.session_state.last_human = human_choice
    st.session_state.last_ai = ai_choice
    st.session_state.last_result = result
    st.session_state.last_reason = reason
    st.session_state.round += 1

    if result == "p1":
        st.session_state.wins += 1
    elif result == "p2":
        st.session_state.losses += 1
    else:
        st.session_state.ties += 1


# ─────────────────────────────────────────
# LEADERBOARD
# ─────────────────────────────────────────
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return {}
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)


def save_to_leaderboard():
    s = st.session_state
    total = s.wins + s.losses + s.ties
    wr = round((s.wins / total) * 100, 1) if total > 0 else 0
    board = load_leaderboard()
    if s.player_name in board:
        board[s.player_name]["wins"] += s.wins
        board[s.player_name]["losses"] += s.losses
        board[s.player_name]["ties"] += s.ties
        t2 = board[s.player_name]["wins"] + board[s.player_name]["losses"] + board[s.player_name]["ties"]
        board[s.player_name]["win_rate"] = round((board[s.player_name]["wins"] / t2) * 100, 1)
    else:
        board[s.player_name] = {"wins": s.wins, "losses": s.losses, "ties": s.ties, "win_rate": wr}
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(board, f, indent=4)
    st.success("✅ Score saved to leaderboard!")


# ─────────────────────────────────────────
# UI LAYOUT
# ─────────────────────────────────────────
st.markdown('<div class="title-glow">🪨 RPS ULTIMATE 🖖</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#ffffff66;font-size:0.9rem;">Rock · Paper · Scissors · Lizard · Spock</p>', unsafe_allow_html=True)

st.divider()

# Sidebar — settings
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.session_state.player_name = st.text_input("Your Name", value=st.session_state.player_name)
    st.session_state.difficulty = st.selectbox(
        "AI Difficulty",
        ["easy", "medium", "hard"],
        index=["easy","medium","hard"].index(st.session_state.difficulty)
    )

    st.divider()
    st.markdown("### 📊 Session Score")
    s = st.session_state
    total = s.wins + s.losses + s.ties
    wr = round((s.wins / total) * 100, 1) if total > 0 else 0
    st.metric("🏆 Wins", s.wins)
    st.metric("💀 Losses", s.losses)
    st.metric("🤝 Ties", s.ties)
    st.metric("📈 Win Rate", f"{wr}%")

    st.divider()
    if st.button("💾 Save to Leaderboard"):
        save_to_leaderboard()

    if st.button("🔄 Reset Score"):
        for k in ["wins","losses","ties","round","last_human","last_ai","last_result","last_reason"]:
            st.session_state[k] = 0 if k in ["wins","losses","ties","round"] else None
        st.rerun()

# Round counter
st.markdown(f"<p style='text-align:center;color:#00ffcc88;font-family:Orbitron,monospace;'>ROUND {st.session_state.round + 1}</p>", unsafe_allow_html=True)

# Choice buttons
st.markdown("#### 👇 Choose your weapon:")
cols = st.columns(5)
for i, choice in enumerate(CHOICES):
    with cols[i]:
        if st.button(f"{EMOJIS[choice]}\n{choice.capitalize()}", key=choice):
            play_round(choice)

st.divider()

# Result display
if st.session_state.last_result is not None:
    h = st.session_state.last_human
    a = st.session_state.last_ai
    r = st.session_state.last_result
    reason = st.session_state.last_reason

    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        st.markdown(f"<div style='text-align:center;font-size:4rem'>{EMOJIS[h]}</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:#00ffcc'>YOU<br>{h.upper()}</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='text-align:center;font-size:2rem;padding-top:1.5rem'>⚔️</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='text-align:center;font-size:4rem'>{EMOJIS[a]}</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:#ff6688'>AI<br>{a.upper()}</p>", unsafe_allow_html=True)

    if r == "p1":
        st.markdown(f'<div class="result-win">🏆 YOU WIN! · {reason}</div>', unsafe_allow_html=True)
    elif r == "p2":
        st.markdown(f'<div class="result-lose">💀 AI WINS! · {reason}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="result-tie">🤝 TIE! · {reason}</div>', unsafe_allow_html=True)

st.divider()

# Rules expander
with st.expander("📖 See all rules"):
    rules_text = [
        "✂️ Scissors cuts Paper", "📄 Paper covers Rock",
        "🪨 Rock crushes Lizard", "🦎 Lizard poisons Spock",
        "🖖 Spock smashes Scissors", "✂️ Scissors decapitates Lizard",
        "🦎 Lizard eats Paper", "📄 Paper disproves Spock",
        "🖖 Spock vaporizes Rock", "🪨 Rock crushes Scissors",
    ]
    for rule in rules_text:
        st.write(rule)

# Leaderboard
with st.expander("🏆 All-Time Leaderboard"):
    board = load_leaderboard()
    if not board:
        st.info("No records yet. Save your score!")
    else:
        sorted_board = sorted(board.items(), key=lambda x: x[1]["win_rate"], reverse=True)
        medals = ["🥇", "🥈", "🥉"]
        for rank, (name, stats) in enumerate(sorted_board):
            medal = medals[rank] if rank < 3 else f"#{rank+1}"
            st.write(f"{medal} **{name}** — W:{stats['wins']} L:{stats['losses']} T:{stats['ties']} ({stats['win_rate']}%)")