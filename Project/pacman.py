from random import choice
from turtle import *
from freegames import floor, vector

state = {'score': 0, 'level': 1}
game_running = True
current_level = 1

path = Turtle(visible=False) #draws maze
writer = Turtle(visible=False) #shows score and messages 

aim = vector(5, 0) #direction of pacman
pacman = vector(-40, -80)  #pacman position 

# Level configurations
LEVEL_CONFIGS = {
    1: {'ghost_speed': 5, 'num_ghosts': 4, 'ghost_delay': 100, 'ghost_colors': ['red', 'red', 'red', 'red']},
    2: {'ghost_speed': 6, 'num_ghosts': 5, 'ghost_delay': 90, 'ghost_colors': ['red', 'red', 'orange', 'orange', 'pink']},
    3: {'ghost_speed': 7, 'num_ghosts': 6, 'ghost_delay': 80, 'ghost_colors': ['red', 'red', 'orange', 'pink', 'purple', 'cyan']},
    4: {'ghost_speed': 8, 'num_ghosts': 7, 'ghost_delay': 70, 'ghost_colors': ['red', 'orange', 'pink', 'purple', 'cyan', 'green', 'yellow']},
    5: {'ghost_speed': 10, 'num_ghosts': 8, 'ghost_delay': 60, 'ghost_colors': ['red', 'orange', 'pink', 'purple', 'cyan', 'green', 'yellow', 'white']}
}

# Ghost spawn positions (different starting locations)
ghost_spawns = [
    vector(-180, 160),   # top-left
    vector(-180, -160),  # bottom-left
    vector(100, 160),    # top-right
    vector(100, -160),   # bottom-right
    vector(-80, 80),     # center-left
    vector(-80, -80),    # center-bottom
    vector(20, 80),      # center-top
    vector(20, -80),     # center-right
]

ghosts = []  # Will be initialized based on level

original_tiles = [
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,
    0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,
    0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,
    0,1,0,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,0,0,
    0,1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,0,0,0,0,
    0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,
    0,1,0,0,1,0,1,1,1,1,1,0,1,0,0,0,0,0,0,0,
    0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0,
    0,0,0,0,1,0,1,1,1,1,1,0,1,0,0,1,0,0,0,0,
    0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,0,0,
    0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,
    0,1,0,0,1,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,
    0,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,0,0,0,0,
    0,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,
    0,1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,0,0,0,0,
    0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,
    0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
]

tiles = original_tiles.copy()

def save_score(score, level):
    with open("pac_score.txt", "a") as file:
        file.write(f"Level {level}: {score}\n")

def reset_tiles():
    global tiles
    tiles = original_tiles.copy()

def init_ghosts():
    global ghosts, current_level
    config = LEVEL_CONFIGS[current_level]
    num_ghosts = config['num_ghosts']
    ghost_speed = config['ghost_speed']
    ghost_colors = config['ghost_colors']
    
    ghosts = []
    directions = [vector(5, 0), vector(-5, 0), vector(0, 5), vector(0, -5)]
    
    for i in range(num_ghosts):
        spawn_index = i % len(ghost_spawns)
        start_pos = ghost_spawns[spawn_index].copy()
        
        # Alternate directions for variety
        dir_index = i % len(directions)
        direction = directions[dir_index].copy()
        direction.x = direction.x * (ghost_speed / 5)  # Scale speed
        direction.y = direction.y * (ghost_speed / 5)
        
        ghosts.append([start_pos, direction, ghost_colors[i % len(ghost_colors)]])
    
    # For backward compatibility with existing code
    # Convert to old format (just position and course)
    old_format_ghosts = []
    for ghost in ghosts:
        old_format_ghosts.append([ghost[0], ghost[1]])
    
    return old_format_ghosts

def exit_game():
    """Exit the game gracefully"""
    global game_running
    
    # Ask for confirmation
    answer = textinput(
        "Exit Game",
        f"Are you sure you want to exit?\n\nFinal Score: {state['score']} (Level {current_level})\n\nScores have been saved.\n\nClick OK to exit, Cancel to continue playing."
    )
    
    if answer is not None:  # User clicked OK
        # Save final score
        save_score(state['score'], current_level)
        
        # Display goodbye message
        writer.clear()
        writer.goto(0, 0)
        writer.write("Thanks for playing!", align="center", font=("Arial", 20, "bold"))
        writer.goto(0, -30)
        writer.write(f"Final Score: {state['score']}", align="center", font=("Arial", 14, "normal"))
        writer.goto(0, -60)
        writer.write("Closing game...", align="center", font=("Arial", 12, "normal"))
        update()
        
        # Wait a moment then close
        ontimer(lambda: bye(), 1500)
        game_running = False
        return True
    else:  # User clicked Cancel
        # Resume game
        return False

def select_level():
    global current_level, game_running
    
    game_running = False  # Pause current game
    
    level_options = "1: Easy\n2: Medium\n3: Hard\n4: Expert\n5: Nightmare"
    answer = textinput(
        "Select Level",
        f"Choose your level:\n{level_options}\n\nCurrent Level: {current_level}\n\nEnter level number (1-5):\n\nPress Cancel to continue playing."
    )
    
    if answer and answer.isdigit():
        level_num = int(answer)
        if 1 <= level_num <= 5:
            current_level = level_num
            state['level'] = current_level
            
            # Show level info
            writer.goto(0, 50)
            writer.write(f"LEVEL {current_level} SELECTED!", align="center", font=("Arial", 14, "bold"))
            ontimer(lambda: writer.clear(), 1500)
            
            restart_game()
            return True
        else:
            writer.goto(0, 50)
            writer.write("Invalid level! Using current level.", align="center", font=("Arial", 12, "normal"))
            ontimer(lambda: writer.clear(), 1500)
            restart_game()
            return False
    else:
        restart_game()
        return False

def restart_game():
    global pacman, aim, game_running, tiles, ghosts, current_level
    
    # Reset game state
    pacman = vector(-40, -80)
    aim = vector(5, 0)
    state['score'] = 0
    game_running = True
    
    # Initialize ghosts based on current level
    ghosts = init_ghosts()
    
    # Reset tiles
    tiles = original_tiles.copy()
    
    # Clear and redraw everything
    writer.clear()
    writer.goto(160, 160)
    writer.write(f"Score: {state['score']}")
    
    # Show level indicator
    writer.goto(-180, 160)
    writer.write(f"Level: {current_level}")
    
    # Show controls reminder
    writer.goto(-180, -180)
    writer.write("Controls: Arrows | L:Level | Esc:Exit", font=("Arial", 8, "normal"))
    
    clear()
    world()
    
    # Re-establish keyboard listeners
    listen()
    onkey(lambda: change(5, 0), 'Right')
    onkey(lambda: change(-5, 0), 'Left')
    onkey(lambda: change(0, 5), 'Up')
    onkey(lambda: change(0, -5), 'Down')
    onkey(select_level, 'l')  # Press 'L' to change level
    onkey(select_level, 'L')
    onkey(exit_game, 'Escape')  # Press 'Esc' to exit game
    onkey(exit_game, 'q')  # Press 'Q' to exit game
    onkey(exit_game, 'Q')
    
    # Start the game loop
    move()

def square(x, y):
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()
    for _ in range(4):
        path.forward(20)
        path.left(90)
    path.end_fill()

def offset(point):
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    return int(x + y * 20)

def valid(point):
    index = offset(point)
    if tiles[index] == 0:
        return False
    
    index = offset(point + 19)
    if tiles[index] == 0:
        return False
    
    return point.x % 20 == 0 or point.y % 20 == 0

def world():
    bgcolor('black')
    path.color('blue')
    
    for index in range(len(tiles)):
        if tiles[index] > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)
            
            if tiles[index] == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

def move():
    global game_running, current_level
    
    if not game_running:
        return
    
    writer.undo()
    writer.goto(160, 160)
    writer.write(f"Score: {state['score']}")
    
    clear()
    
    if valid(pacman + aim):
        pacman.move(aim)
    
    index = offset(pacman)
    
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)
    
    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')
    
    # Draw ghosts with different colors
    for i, ghost_data in enumerate(ghosts):
        point, course = ghost_data[0], ghost_data[1]
        
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(5, 0), vector(-5, 0),
                vector(0, 5), vector(0, -5)
            ]
            plan = choice(options)
            # Scale direction based on level speed
            speed_multiplier = LEVEL_CONFIGS[current_level]['ghost_speed'] / 5
            course.x = plan.x * speed_multiplier
            course.y = plan.y * speed_multiplier
        
        up()
        goto(point.x + 10, point.y + 10)
        
        # Get ghost color (for backward compatibility with old format)
        if len(ghost_data) > 2:
            color = ghost_data[2]
        else:
            color = 'red'
        
        dot(20, color)
    
    update()
    
    # Check collision with ghosts
    for ghost_data in ghosts:
        point, course = ghost_data[0], ghost_data[1]
        if abs(pacman - point) < 20:
            game_running = False
            save_score(state['score'], current_level)
            
            writer.goto(0, 0)
            writer.write(f"GAME OVER - Level {current_level}", align="center", font=("Arial", 16, "bold"))
            
            writer.goto(0, -30)
            writer.write(f"Score: {state['score']}", align="center", font=("Arial", 12, "normal"))
            
            writer.goto(0, -60)
            writer.write("Press R to restart | L for level | Esc to exit", align="center", font=("Arial", 10, "normal"))
            
            # Add restart, level select, and exit keys
            onkey(restart_game, 'r')
            onkey(restart_game, 'R')
            onkey(select_level, 'l')
            onkey(select_level, 'L')
            onkey(exit_game, 'Escape')
            onkey(exit_game, 'q')
            onkey(exit_game, 'Q')
            return
    
    # Level up condition (every 50 points)
    if state['score'] > 0 and state['score'] % 50 == 0:
        new_level = min(5, (state['score'] // 50) + 1)
        if new_level > current_level:
            current_level = new_level
            state['level'] = current_level
            writer.goto(0, 50)
            writer.write(f"LEVEL UP! Now Level {current_level}", align="center", font=("Arial", 14, "bold"))
            ontimer(lambda: writer.clear(), 1500)
            # Restart with new level
            restart_game()
            return
    
    # Use level-specific delay for ghost movement speed
    move_delay = LEVEL_CONFIGS[current_level]['ghost_delay']
    ontimer(move, move_delay)

def ask_restart():
    answer = textinput(
        "Game Over",
        f"Score: {state['score']} (Level {current_level})\n\nRestart? (yes/no)\n\nPress 'L' for level select\nPress 'Esc' to exit"
    )
    
    if answer and answer.lower() == "yes":
        restart_game()
    elif answer and answer.lower() == "no":
        print(f"Game Over! Final Score: {state['score']} on Level {current_level}")
        print("Scores saved in pac_score.txt")
        exit_game()
    else:
        # Wait for key press
        onkey(restart_game, 'r')
        onkey(restart_game, 'R')
        onkey(select_level, 'l')
        onkey(select_level, 'L')
        onkey(exit_game, 'Escape')
        onkey(exit_game, 'q')
        onkey(exit_game, 'Q')

def change(x, y):
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

# SETUP
setup(420, 420, 370, 0)
hideturtle()
tracer(False)

writer.goto(160, 160)
writer.color('white')
writer.write(f"Score: {state['score']}")

writer.goto(-180, 160)
writer.write(f"Level: {current_level}")

writer.goto(-180, -180)
writer.write("Controls: Arrows | L:Level | Esc:Exit", font=("Arial", 8, "normal"))

writer.goto(0, 100)
writer.write("PACMAN", align="center", font=("Arial", 20, "bold"))
writer.goto(0, 70)
writer.write("Press L to select level", align="center", font=("Arial", 10, "normal"))
writer.goto(0, 50)
writer.write("Press Esc to exit", align="center", font=("Arial", 10, "normal"))

listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
onkey(select_level, 'l')
onkey(select_level, 'L')
onkey(exit_game, 'Escape')  # Exit with Escape key
onkey(exit_game, 'q')  # Exit with Q key
onkey(exit_game, 'Q')

# Initialize ghosts
ghosts = init_ghosts()

world()
move()
done()