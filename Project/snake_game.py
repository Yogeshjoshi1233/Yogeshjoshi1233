import turtle
import random
import time
import os

# Game variables
snake_segments = []
food = None
direction = "right"
next_direction = "right"
score = 0
level = 1
game_active = False
paused = False
game_loop_id = None

# Score file
SCORE_FILE = "snake_score.txt"

# Level settings
LEVELS = {
    1: {"speed": 150, "points": 10, "name": "Easy"},
    2: {"speed": 120, "points": 20, "name": "Medium"},
    3: {"speed": 90, "points": 30, "name": "Hard"},
    4: {"speed": 70, "points": 50, "name": "Expert"},
    5: {"speed": 50, "points": 70, "name": "Insane"}
}

def save_score(final_score, level_reached):
    """Save score to file"""
    with open(SCORE_FILE, "a") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - Score: {final_score} - Level: {LEVELS[level_reached]['name']}\n")

def get_high_score():
    """Get highest score from file"""
    if not os.path.exists(SCORE_FILE):
        return 0
    
    high_score = 0
    with open(SCORE_FILE, "r") as f:
        for line in f:
            try:
                if "Score:" in line:
                    score_part = line.split("Score:")[1].split("-")[0].strip()
                    score_value = int(score_part)
                    if score_value > high_score:
                        high_score = score_value
            except:
                continue
    return high_score

# Screen setup
screen = turtle.Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("Snake Game - Level Edition")
screen.tracer(0)
screen.listen()

# Create turtles for display
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.color("white")

def show_menu():
    """Display main menu"""
    global game_active, paused, game_loop_id
    game_active = False
    paused = False
    
    if game_loop_id:
        screen.ontimer(None, game_loop_id)
        game_loop_id = None
    
    clear_snake()
    if food:
        food.hideturtle()
    
    pen.clear()
    
    high_score = get_high_score()
    
    pen.goto(0, 220)
    pen.write("SNAKE GAME", align="center", font=("Arial", 28, "bold"))
    
    pen.goto(0, 190)
    pen.write(f"High Score: {high_score}", align="center", font=("Arial", 14, "normal"))
    
    y = 120
    for num, info in LEVELS.items():
        pen.goto(-200, y)
        pen.write(f"{num}. {info['name']} - Speed: {info['speed']}ms - {info['points']} pts/food", 
                 align="left", font=("Arial", 13, "normal"))
        y -= 30
    
    pen.goto(0, -50)
    pen.write("Press 1-5 to select level", align="center", font=("Arial", 16, "bold"))
    pen.goto(0, -90)
    pen.write("Press Q to quit", align="center", font=("Arial", 14, "normal"))
    
    screen.update()

def clear_snake():
    """Remove all snake segments from screen"""
    global snake_segments
    for segment in snake_segments:
        segment.hideturtle()
        segment.clear()
    snake_segments.clear()

def start_game(selected_level):
    """Initialize and start the game"""
    global snake_segments, food, direction, next_direction, score, level, game_active, paused, game_loop_id
    
    if game_loop_id:
        screen.ontimer(None, game_loop_id)
        game_loop_id = None
    
    clear_snake()
    pen.clear()
    if food:
        food.hideturtle()
    
    level = selected_level
    score = 0
    direction = "right"
    next_direction = "right"
    game_active = True
    paused = False
    
    snake_segments = []
    start_x = 0
    start_y = 0
    
    for i in range(3):
        segment = turtle.Turtle()
        segment.shape("square")
        segment.penup()
        segment.goto(start_x - (i * 20), start_y)
        snake_segments.append(segment)
    
    snake_segments[0].color("light green")
    for i in range(1, len(snake_segments)):
        snake_segments[i].color("dark green")
    
    food = turtle.Turtle()
    food.shape("circle")
    food.color("red")
    food.penup()
    generate_food()
    
    update_hud()
    game_loop()

def generate_food():
    """Generate food at random position not on snake"""
    if not food:
        return
    
    while True:
        x = random.randint(-14, 14) * 20
        y = random.randint(-14, 14) * 20
        
        collision = False
        for segment in snake_segments:
            if segment.xcor() == x and segment.ycor() == y:
                collision = True
                break
        
        if not collision:
            food.goto(x, y)
            break

def update_hud():
    """Update score and level display"""
    pen.clear()
    pen.color("white")
    pen.goto(-280, 260)
    pen.write(f"Level: {LEVELS[level]['name']}", align="left", font=("Arial", 12, "normal"))
    pen.goto(-280, 235)
    pen.write(f"Score: {score}", align="left", font=("Arial", 12, "normal"))
    pen.goto(-280, 210)
    pen.write(f"Length: {len(snake_segments)}", align="left", font=("Arial", 12, "normal"))
    
    high_score = get_high_score()
    pen.goto(200, 260)
    pen.write(f"High Score: {high_score}", align="right", font=("Arial", 12, "normal"))
    
    if paused:
        pen.goto(0, 0)
        pen.write("PAUSED", align="center", font=("Arial", 24, "bold"))
    
    screen.update()

def move_snake():
    """Move the snake in current direction"""
    global direction, next_direction, score
    
    if not game_active or paused:
        return True
    
    direction = next_direction
    head = snake_segments[0]
    head_x = head.xcor()
    head_y = head.ycor()
    
    if direction == "up":
        new_x = head_x
        new_y = head_y + 20
    elif direction == "down":
        new_x = head_x
        new_y = head_y - 20
    elif direction == "left":
        new_x = head_x - 20
        new_y = head_y
    else:
        new_x = head_x + 20
        new_y = head_y
    
    if new_x > 280 or new_x < -280 or new_y > 280 or new_y < -280:
        game_over()
        return False
    
    for segment in snake_segments:
        if segment.xcor() == new_x and segment.ycor() == new_y:
            game_over()
            return False
    
    new_head = turtle.Turtle()
    new_head.shape("square")
    new_head.color("light green")
    new_head.penup()
    new_head.goto(new_x, new_y)
    snake_segments.insert(0, new_head)
    
    if snake_segments[0].xcor() == food.xcor() and snake_segments[0].ycor() == food.ycor():
        points = LEVELS[level]["points"]
        score += points
        generate_food()
        update_hud()
        
        if score % 100 == 0 and score > 0 and level < len(LEVELS):
            level_up()
    else:
        tail = snake_segments.pop()
        tail.hideturtle()
        tail.clear()
    
    for i, segment in enumerate(snake_segments):
        if i == 0:
            segment.color("light green")
        else:
            segment.color("dark green")
    
    return True

def level_up():
    """Increase level"""
    global level, game_active
    level += 1
    
    pen.goto(0, 50)
    pen.write(f"LEVEL UP! {LEVELS[level]['name']}", align="center", font=("Arial", 20, "bold"))
    screen.update()
    time.sleep(1)
    pen.clear()
    update_hud()

def game_over():
    """Handle game over"""
    global game_active, game_loop_id, score, level
    
    game_active = False
    
    # Save score to file
    save_score(score, level)
    high_score = get_high_score()
    
    if game_loop_id:
        screen.ontimer(None, game_loop_id)
        game_loop_id = None
    
    pen.goto(0, 100)
    pen.write("GAME OVER!", align="center", font=("Arial", 24, "bold"))
    pen.goto(0, 60)
    pen.write(f"Final Score: {score}", align="center", font=("Arial", 18, "normal"))
    pen.goto(0, 25)
    pen.write(f"High Score: {high_score}", align="center", font=("Arial", 16, "normal"))
    pen.goto(0, -10)
    pen.write(f"Level Reached: {LEVELS[level]['name']}", align="center", font=("Arial", 14, "normal"))
    pen.goto(0, -50)
    pen.write("Press R to restart same level", align="center", font=("Arial", 13, "normal"))
    pen.goto(0, -80)
    pen.write("Press M for main menu", align="center", font=("Arial", 13, "normal"))
    pen.goto(0, -110)
    pen.write("Press Q to quit", align="center", font=("Arial", 13, "normal"))
    screen.update()

def restart_game():
    """Restart current level"""
    if not game_active:
        start_game(level)

def return_to_menu():
    """Return to main menu from anywhere"""
    global game_active, paused, game_loop_id
    
    if game_loop_id:
        screen.ontimer(None, game_loop_id)
        game_loop_id = None
    
    game_active = False
    paused = False
    clear_snake()
    if food:
        food.hideturtle()
    show_menu()

def set_direction(new_direction):
    """Set snake direction with restrictions"""
    global next_direction
    
    if not game_active or paused:
        return
    
    if (direction == "up" and new_direction == "down") or \
       (direction == "down" and new_direction == "up") or \
       (direction == "left" and new_direction == "right") or \
       (direction == "right" and new_direction == "left"):
        return
    
    next_direction = new_direction

def toggle_pause():
    """Pause/unpause the game"""
    global paused
    if game_active:
        paused = not paused
        update_hud()
        if not paused:
            game_loop()

def exit_game():
    """Exit the game"""
    clear_snake()
    if food:
        food.hideturtle()
    screen.bye()

def game_loop():
    """Main game loop"""
    global game_loop_id
    
    if game_active and not paused:
        if move_snake():
            update_hud()
            screen.update()
            game_loop_id = screen.ontimer(game_loop, LEVELS[level]["speed"])
        else:
            return
    elif game_active and paused:
        game_loop_id = screen.ontimer(game_loop, 100)
    else:
        return

# Keyboard bindings
screen.onkeypress(lambda: set_direction("up"), "Up")
screen.onkeypress(lambda: set_direction("down"), "Down")
screen.onkeypress(lambda: set_direction("left"), "Left")
screen.onkeypress(lambda: set_direction("right"), "Right")
screen.onkeypress(toggle_pause, "p")
screen.onkeypress(toggle_pause, "P")
screen.onkeypress(restart_game, "r")
screen.onkeypress(restart_game, "R")
screen.onkeypress(return_to_menu, "m")
screen.onkeypress(return_to_menu, "M")
screen.onkeypress(exit_game, "q")
screen.onkeypress(exit_game, "Q")

screen.onkeypress(lambda: start_game(1), "1")
screen.onkeypress(lambda: start_game(2), "2")
screen.onkeypress(lambda: start_game(3), "3")
screen.onkeypress(lambda: start_game(4), "4")
screen.onkeypress(lambda: start_game(5), "5")

show_menu()
screen.mainloop()