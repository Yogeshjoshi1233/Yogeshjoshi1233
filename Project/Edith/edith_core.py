import time
import sys
from pathlib import Path
import logging
from edith_speaker import EdithSpeaker
from edith_commander import EdithCommander
from edith_memory import EdithMemory
from edith_skills import EdithSkills

# Setup logging
LOG_DIR = Path("data/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - EDITH - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'edith.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EdithCore:
    """Main EDITH engine - Text Input, Voice Output"""
    
    def __init__(self):
        self.running = True
        
        # Initialize all modules
        logger.info("Initializing EDITH modules...")
        self.speaker = EdithSpeaker()
        self.memory = EdithMemory()
        self.skills = EdithSkills()
        self.commander = EdithCommander(self.skills, self.memory)
        
        logger.info("EDITH Core initialized successfully")
        print("\n" + "="*50)
        print("    EDITH - Even Dead, I'm The Hero")
        print("="*50)
        print("Type your commands below.")
        print("Type 'exit' or 'quit' to stop.")
        print("="*50 + "\n")
    
    def start(self):
        """Start EDITH - Main loop"""
        self.speaker.speak("EDITH online. Type your commands.")
        logger.info("EDITH starting up...")
        
        # Main command loop
        while self.running:
            try:
                # Get text input from user
                command = input("\nYou: ").strip()
                
                if not command:
                    continue
                
                # Check for exit command
                if command.lower() in ["exit", "quit", "goodbye", "bye"]:
                    self.shutdown()
                    break
                
                # Process the command
                logger.info(f"Command: {command}")
                response = self.commander.process(command)
                
                if response:
                    self.speaker.speak(response)
                    self.memory.add_interaction(command, response)
                else:
                    self.speaker.speak("I'm not sure how to handle that. Try 'help'.")
                
            except KeyboardInterrupt:
                self.shutdown()
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                self.speaker.speak("Sorry, I encountered an error.")
    
    def shutdown(self):
        """Graceful shutdown"""
        self.running = False
        self.speaker.speak("Goodbye!")
        logger.info("EDITH shutdown complete")
        sys.exit(0)

if __name__ == "__main__":
    edith = EdithCore()
    edith.start()