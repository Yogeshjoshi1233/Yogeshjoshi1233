import os
import subprocess
import sys
import platform
def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def display_header():
    print(" " * 20 + "---- GAME ZONE ----")
    
def run_snake_game():
    print("\n1: Launching Snake Game")
    try:
        subprocess.run([sys.executable, "snake_game.py"])#Path of the python interpreter currently running  
        
    except FileNotFoundError:
        print("ERROR: snake_game.py not found!")
        input("Press Enter to continue...")
    except Exception as e: # catch any error that happens and store it in variable e 
        print("error:",e)
        input("Press Enter to continue...")

def run_pacman():
    
    print("\n2:  Launching Pacman")
    
    try:
        subprocess.run([sys.executable, "pacman.py"])
    except FileNotFoundError:
        print("ERROR: pacman.py not found!")
        input("Press Enter to continue...")
    except Exception as e:
        print("error:",e)
        input("Press Enter to continue...")

def run_car_racing():
    
    print("\n3 : Launching Car Racing")
    
    try:
        subprocess.run([sys.executable, "car_racing.py"])
    except FileNotFoundError:
        print("ERROR: car_racing.py not found!")
        input("Press Enter to continue...")
    except Exception as e:
        print("error:",e)
        input("Press Enter to continue...")

def run_tic_tac_toe():
    
    print("\n 4 : sLaunching Tic Tac Toe")
    
    try:
        subprocess.run([sys.executable, "tic_tac_toe.py"])
    except FileNotFoundError:
        print("ERROR: tic_tac_toe.py not found!")
        input("Press Enter to continue")
    except Exception as e:
        print("ERROR:",e)
        input("Press Enter to continue")

def main():
    
    while True:
        clear_screen()
        display_header()
        
        print("\nSelect a game to play:")
        
        print("  1. Snake Game")
        print("  2. Pacman")
        print("  3. Car Racing")
        print("  4. Tic Tac Toe")
        print("  5. Exit")
        
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            run_snake_game()
        elif choice == "2":
            run_pacman()
        elif choice == "3":
            run_car_racing()
        elif choice == "4":
            run_tic_tac_toe()
        elif choice == "5":
            clear_screen()
            print("=" * 40)
            print("Thank you for playing! Goodbye!")
            print("=" * 40)
            break
        else:
            print("\nInvalid choice! Please enter 1, 2, 3, 4, or 5")
            input("\nPress Enter to continue")

if __name__ == "__main__":
    main()