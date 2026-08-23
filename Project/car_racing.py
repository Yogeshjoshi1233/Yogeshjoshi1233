import turtle 
import random 
import time
import os
FILE_NAME = "race_score.txt"
win = turtle.Screen() 
win.title("Rush Road")
win.bgcolor("black")
win.setup(width=400, height=600)
win.tracer(0)

lanes = [-120, -40, 40, 120]

# Player
player = turtle.Turtle()
player.shape("square")
player.color("white")
player.shapesize(stretch_wid=1.5, stretch_len=1.5)
player.penup()  

# Score display
pen = turtle.Turtle()
pen.hideturtle()
pen.color("white")
pen.penup()
pen.goto(0, 260)

# Level display
level_pen = turtle.Turtle()
level_pen.hideturtle()
level_pen.color("yellow")
level_pen.penup()
level_pen.goto(0, 230)

# Variables
player_lane = 1
score = 0
enemies = [] 
game_running = True
score_saved = False
current_level = 1  # This will be set by user and NEVER change

# Level settings (FIXED - no progression)
LEVEL_SETTINGS = {
    1: {"enemy_speed": 15, "spawn_rate": 3, "color": "green", "name": "Easy"},
    2: {"enemy_speed": 20, "spawn_rate": 2, "color": "yellow", "name": "Normal"},
    3: {"enemy_speed": 25, "spawn_rate": 1, "color": "orange", "name": "Hard"},
    4: {"enemy_speed": 30, "spawn_rate": 1, "color": "red", "name": "Expert"},
    5: {"enemy_speed": 35, "spawn_rate": 0, "color": "purple", "name": "Insane"}
}

def save_score(score):
    with open(FILE_NAME, "a") as f:
        f.write(str(score) + "\n") 

def get_high_score():
    if not os.path.exists(FILE_NAME):
        return 0
    
    with open(FILE_NAME, "r") as f:
        scores = [int(line.strip()) for line in f if line.strip().isdigit()]
    
    return max(scores) if scores else 0

def update_score():
    pen.clear()
    high = get_high_score()
    pen.write(f"Score: {score}   High Score: {high}",
              align="center", font=("Arial", 16, "bold"))

def update_level_display():
    level_pen.clear()
    level_info = LEVEL_SETTINGS[current_level]
    level_pen.write(f"Level: {current_level} - {level_info['name']} [{level_info['color'].upper()}]",
                    align="center", font=("Arial", 12, "bold"))

def move_left():
    global player_lane
    if game_running and player_lane > 0:
        player_lane -= 1 
        player.setx(lanes[player_lane])

def move_right():
    global player_lane
    if game_running and player_lane < 3:
        player_lane += 1
        player.setx(lanes[player_lane])

def spawn_enemy():
    level_info = LEVEL_SETTINGS[current_level]
    # Higher levels = more frequent spawning
    spawn_chance = level_info["spawn_rate"]
    if random.randint(0, spawn_chance) == 0:
        enemy = turtle.Turtle()
        enemy.shape("square")
        enemy.color(level_info["color"])  # Enemy color matches level
        enemy.penup()
        lane = random.randint(0, 3)
        enemy.goto(lanes[lane], 300)
        enemies.append(enemy)

def move_enemies():
    global score, game_running, score_saved
    
    level_info = LEVEL_SETTINGS[current_level]
    
    for enemy in enemies[:]:
        enemy.sety(enemy.ycor() - level_info["enemy_speed"])
        
        # COLLISION → SAVE SCORE IMMEDIATELY
        if enemy.distance(player) < 20:
            if not score_saved:
                save_score(score)
                score_saved = True
            game_running = False
        
        # Enemy passed (score increases but NO level up)
        if enemy.ycor() < -300:
            enemy.hideturtle()
            enemies.remove(enemy)
            score += 1

def game_over_screen():
    pen.goto(0, 0)
    level_info = LEVEL_SETTINGS[current_level]
    pen.write(f"GAME OVER\nScore: {score}\nLevel: {current_level} - {level_info['name']}",
              align="center", font=("Arial", 18, "bold"))

def reset_game():
    global player_lane, score, enemies, game_running, score_saved
    
    for enemy in enemies:
        enemy.hideturtle() 
    enemies.clear()
    
    player_lane = 1
    score = 0
    game_running = True 
    score_saved = False
    
    player.goto(lanes[player_lane], -250)
    player.color("white")
    pen.clear()
    level_pen.clear()
    update_level_display()
    update_score()

def draw_road():
    road = turtle.Turtle()
    road.hideturtle()
    road.color("gray")
    road.penup()
    
    for x in lanes: 
        road.goto(x, -300)
        road.setheading(90) 
        for _ in range(30):
            road.pendown()
            road.forward(10)
            road.penup()
            road.forward(10)

def start_game():
    global current_level, game_running
    
    # Reset game state
    game_running = True
    
    # Clear any existing turtles
    for enemy in enemies[:]:
        enemy.hideturtle()
    enemies.clear()
    
    # Reset player position and color
    player.goto(lanes[player_lane], -250)
    player.color("white")
    player.showturtle()
    
    # Draw road
    draw_road()
    
    # Update displays
    update_level_display()
    update_score()
    
    # Controls
    win.listen()
    win.onkeypress(move_left, "a")
    win.onkeypress(move_right, "d")
    
    # Game loop
    while True:
        win.update()
        
        # Dynamic game speed based on level (fixed for the chosen level)
        sleep_time = max(0.05, 0.1 - (current_level * 0.005))
        time.sleep(sleep_time)
        
        if game_running:
            spawn_enemy()
            move_enemies()
            update_score()
        else:
            game_over_screen()
            
            answer = win.textinput("Play Again", "Do you want to play again? (yes/no)")
            
            if answer and answer.lower() == "yes":
                reset_game()
                # Ask if they want to change level for next game
                change_level = win.textinput("Change Level", 
                                            "Do you want to change level? (yes/no)")
                if change_level and change_level.lower() == "yes":
                    # Level selection without clearing screen
                    selected = win.textinput("Level Selection", 
                                            "Choose level (1-5):\n"
                                            "1-Easy (Green, Speed 15)\n"
                                            "2-Normal (Yellow, Speed 20)\n"
                                            "3-Hard (Orange, Speed 25)\n"
                                            "4-Expert (Red, Speed 30)\n"
                                            "5-Insane (Purple, Speed 35)")
                    try:
                        new_level = int(selected)
                        if 1 <= new_level <= 5:
                            current_level = new_level
                            update_level_display()
                    except:
                        pass
            else:
                break
    
    turtle.bye()

# Main execution
if __name__ == "__main__":
    # Reset all game variables
    player_lane = 1
    score = 0
    enemies = []
    game_running = True
    score_saved = False
    
    # Show level selection screen
    selection_pen = turtle.Turtle()
    selection_pen.hideturtle()
    selection_pen.color("white")
    selection_pen.penup()
    
    selection_pen.goto(0, 200)
    selection_pen.write("RUSH ROAD", align="center", font=("Arial", 28, "bold"))
    selection_pen.goto(0, 150)
    selection_pen.write("Select Your Difficulty Level", align="center", font=("Arial", 18, "normal"))
    
    # Display level options
    y_pos = 100
    for level in range(1, 6):
        settings = LEVEL_SETTINGS[level]
        selection_pen.goto(0, y_pos)
        selection_pen.write(f"Level {level}: {settings['name']} - {settings['color'].upper()} "
                          f"(Speed: {settings['enemy_speed']}, Spawn Rate: 1/{settings['spawn_rate']+1})",
                          align="center", font=("Arial", 11, "normal"))
        y_pos -= 25
    
    selection_pen.goto(0, -50)
    selection_pen.write("Enter level number (1-5) in the popup box", 
                      align="center", font=("Arial", 14, "bold"))
    
    # Get level selection
    while True:
        try:
            selected = win.textinput("Level Selection", 
                                    "CHOOSE YOUR LEVEL (1-5):\n\n"
                                    "1 - EASY (Green enemies, Slow speed)\n"
                                    "2 - NORMAL (Yellow enemies)\n"
                                    "3 - HARD (Orange enemies, Fast)\n"
                                    "4 - EXPERT (Red enemies, Very fast)\n"
                                    "5 - INSANE (Purple enemies, Maximum difficulty)\n\n"
                                    "The level will NOT change during gameplay!")
            
            if selected is None:  # User cancelled
                selected_level = 1
                break
            
            selected_level = int(selected)
            if 1 <= selected_level <= 5:
                selection_pen.clear()
                break
            else:
                selection_pen.goto(0, -100)
                selection_pen.write("Invalid! Please enter 1-5", 
                                  align="center", font=("Arial", 12, "red"))
                time.sleep(1)
                selection_pen.clear()
                selection_pen.goto(0, 200)
                selection_pen.write("RUSH ROAD", align="center", font=("Arial", 28, "bold"))
                selection_pen.goto(0, 150)
                selection_pen.write("Select Your Difficulty Level", align="center", font=("Arial", 18, "normal"))
                # Redisplay options
                y_pos = 100
                for level in range(1, 6):
                    settings = LEVEL_SETTINGS[level]
                    selection_pen.goto(0, y_pos)
                    selection_pen.write(f"Level {level}: {settings['name']} - {settings['color'].upper()} "
                                      f"(Speed: {settings['enemy_speed']}, Spawn Rate: 1/{settings['spawn_rate']+1})",
                                      align="center", font=("Arial", 11, "normal"))
                    y_pos -= 25
                selection_pen.goto(0, -50)
                selection_pen.write("Enter level number (1-5) in the popup box", 
                                  align="center", font=("Arial", 14, "bold"))
        except ValueError:
            selection_pen.goto(0, -100)
            selection_pen.write("Invalid! Please enter a number 1-5", 
                              align="center", font=("Arial", 12, "red"))
            time.sleep(1)
            selection_pen.clear()
            selection_pen.goto(0, 200)
            selection_pen.write("RUSH ROAD", align="center", font=("Arial", 28, "bold"))
            selection_pen.goto(0, 150)
            selection_pen.write("Select Your Difficulty Level", align="center", font=("Arial", 18, "normal"))
            # Redisplay options
            y_pos = 100
            for level in range(1, 6):
                settings = LEVEL_SETTINGS[level]
                selection_pen.goto(0, y_pos)
                selection_pen.write(f"Level {level}: {settings['name']} - {settings['color'].upper()} "
                                  f"(Speed: {settings['enemy_speed']}, Spawn Rate: 1/{settings['spawn_rate']+1})",
                                  align="center", font=("Arial", 11, "normal"))
                y_pos -= 25
            selection_pen.goto(0, -50)
            selection_pen.write("Enter level number (1-5) in the popup box", 
                              align="center", font=("Arial", 14, "bold"))
    
    selection_pen.clear()
    current_level = selected_level
    
    # Show confirmation message
    confirm_pen = turtle.Turtle()
    confirm_pen.hideturtle()
    confirm_pen.color("green")
    confirm_pen.penup()
    confirm_pen.goto(0, 0)
    level_info = LEVEL_SETTINGS[current_level]
    confirm_pen.write(f"Starting Level {current_level}: {level_info['name']}\nGood Luck!",
                     align="center", font=("Arial", 16, "bold"))
    time.sleep(2)
    confirm_pen.clear()
    
    # Start the game
    start_game()