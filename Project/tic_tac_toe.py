from turtle import *
from freegames import line
import random

FILE_NAME = "score.txt"

board = [None] * 9
score = {'X': 0, 'O': 0, 'Draw': 0}
difficulty = "medium"  # default difficulty
game_mode = "2player"  # "2player" or "vsAI"
ai_player = 1  # AI plays as O (player 1 index is O)

# Load existing score
def load_score():
    global score
    try:
        with open(FILE_NAME, "r") as f:
            data = f.read().split()
            if len(data) == 3:
                score['X'] = int(data[0])
                score['O'] = int(data[1])
                score['Draw'] = int(data[2])
    except FileNotFoundError:
        pass

# Save updated score
def save_score():
    with open(FILE_NAME, "w") as f:
        f.write(f"{score['X']} {score['O']} {score['Draw']}")

def winner():
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] is not None:
            return board[a]
    return None

def draw_check():
    return all(x is not None for x in board)

def show_score():
    print("\n" + "="*40)
    print(f" SCORE BOARD ")
    print(f"  Player X: {score['X']}  |  Player O: {score['O']}  |  Draws: {score['Draw']}")
    print("="*40)

def reset_game():
    global board
    board = [None] * 9
    state['player'] = 0
    state['game_over'] = False
    clear()
    grid()
    update()
    show_score()

def grid():
    line(-67, 200, -67, -200)
    line(67, 200, 67, -200)
    line(-200, -67, 200, -67)
    line(-200, 67, 200, 67)

def drawx(x, y):
    line(x, y, x + 133, y + 133)
    line(x, y + 133, x + 133, y)

def drawo(x, y):
    up()
    goto(x + 67, y + 5)
    down()
    circle(62)

def floor(value):
    return ((value + 200) // 133) * 133 - 200

def index(x, y):
    return int((x + 200) // 133 + ((y + 200) // 133) * 3)

def get_empty_positions():
    return [i for i, cell in enumerate(board) if cell is None]

def ai_move():
    """AI makes a move based on difficulty level"""
    empty_spots = get_empty_positions()
    if not empty_spots:
        return
    
    if difficulty == "easy":
        # Easy: Random move
        move_idx = random.choice(empty_spots)
        
    elif difficulty == "medium":
        # Medium: 70% smart move, 30% random
        if random.random() < 0.7:
            move_idx = get_smart_move()
        else:
            move_idx = random.choice(empty_spots)
            
    else:  # hard
        # Hard: Always smart move
        move_idx = get_smart_move()
    
    # Make the move
    x = (move_idx % 3) * 133 - 200
    y = (move_idx // 3) * 133 - 200
    players[ai_player](x, y)
    update()
    board[move_idx] = ai_player
    
    return move_idx

def get_smart_move():
    """Returns the best move for AI using minimax-like logic"""
    empty_spots = get_empty_positions()
    
    # Check if AI can win
    for spot in empty_spots:
        board[spot] = ai_player
        if winner() == ai_player:
            board[spot] = None
            return spot
        board[spot] = None
    
    # Check if player can win and block
    human_player = 1 - ai_player
    for spot in empty_spots:
        board[spot] = human_player
        if winner() == human_player:
            board[spot] = None
            return spot
        board[spot] = None
    
    # Take center if available
    if 4 in empty_spots:
        return 4
    
    # Take corners
    corners = [0, 2, 6, 8]
    available_corners = [c for c in corners if c in empty_spots]
    if available_corners:
        return random.choice(available_corners)
    
    # Take any edge
    return random.choice(empty_spots)

def check_game_end():
    """Check for win or draw and update game state"""
    win = winner()
    if win is not None:
        winner_name = "X" if win == 0 else "O"
        print(f"\n🎉 Player {winner_name} wins! 🎉")
        score['X' if win == 0 else 'O'] += 1
        save_score()
        show_score()
        state['game_over'] = True
        return True

    if draw_check():
        print("\n🤝 Game Draw! 🤝")
        score['Draw'] += 1
        save_score()
        show_score()
        state['game_over'] = True
        return True
    
    return False

def ai_move_and_check():
    """Handle AI move and subsequent game state"""
    if not state['game_over'] and state['player'] == ai_player:
        ai_move()
        if check_game_end():
            return
        state['player'] = not state['player']

def tap(x, y):
    if state['game_over']:
        ans = textinput("Game Over", "Play again? (yes/no)")
        if ans and ans.lower() == "yes":
            reset_game()
        else:
            bye()
        return

    x = floor(x)
    y = floor(y)
    idx = index(x, y)

    if board[idx] is not None:
        return

    player = state['player']
    players[player](x, y)   
    update()
    board[idx] = player

    # Check win/draw after player move
    if check_game_end():
        return

    # Switch player
    state['player'] = not player
    
    # If in AI mode and game not over, let AI play
    if game_mode == "vsAI" and not state['game_over'] and state['player'] == ai_player:
        # Small delay to make AI move feel natural
        screen = getscreen()
        screen.ontimer(lambda: ai_move_and_check(), 300)

def select_difficulty():
    global difficulty
    print("\n" + "="*40)
    print("🎮 SELECT DIFFICULTY LEVEL 🎮")
    print("  1. Easy (Random moves)")
    print("  2. Medium (Mixed strategy)")
    print("  3. Hard (Perfect play)")
    print("="*40)
    
    while True:
        choice = input("Enter difficulty (1/2/3): ").strip()
        if choice == "1":
            difficulty = "easy"
            break
        elif choice == "2":
            difficulty = "medium"
            break
        elif choice == "3":
            difficulty = "hard"
            break
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3.")
    
    print(f"\n✅ Difficulty set to: {difficulty.upper()}\n")

def select_game_mode():
    global game_mode
    print("\n" + "="*40)
    print("🎮 SELECT GAME MODE 🎮")
    print("  1. Two Players (X vs O)")
    print("  2. VS Computer (X vs AI)")
    print("="*40)
    
    while True:
        choice = input("Enter mode (1/2): ").strip()
        if choice == "1":
            game_mode = "2player"
            break
        elif choice == "2":
            game_mode = "vsAI"
            break
        else:
            print("❌ Invalid choice! Please enter 1 or 2.")
    
    print(f"\n✅ Game mode set to: {'Two Players' if game_mode == '2player' else 'VS Computer'}\n")
    
    if game_mode == "vsAI":
        select_difficulty()

# Game state
state = {'player': 0, 'game_over': False}
players = [drawx, drawo]

# START
load_score()

# Welcome and setup
print("\n" + "="*40)
print("🎯 WELCOME TO TIC TAC TOE! 🎯")
print("="*40)

select_game_mode()

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
grid()
update()

print("\n🎮 Game Started!")
print("   Player X starts first")
if game_mode == "2player":
    print("   Players take turns clicking on the grid")
else:
    print(f"   You are X, AI is O (Difficulty: {difficulty.upper()})")
show_score()

onscreenclick(tap)
done()