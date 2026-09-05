import logging

logger = logging.getLogger(__name__)

class EdithCommander:
    """Command processor"""
    
    def __init__(self, skills, memory):
        self.skills = skills
        self.memory = memory
        logger.info("Commander initialized")
    
    def process(self, command):
        """Process a command and return response"""
        command = command.lower().strip()
        logger.info(f"Processing: {command}")
        
        # Check for help
        if command in ["help", "?"]:
            return self._get_help()
        
        # Check for memory/context
        if "remember" in command or "recall" in command:
            context = self.memory.get_context()
            if context and len(context) > 0:
                last_cmd = context[-1]['command'] if context else "nothing"
                return f"I remember you asked about {last_cmd}"
        
        # Check for reminders
        if "remind" in command:
            parts = command.split("to", 1)
            if len(parts) > 1:
                reminder = parts[1].strip()
                if reminder:
                    self.memory.add_reminder(reminder)
                    return f"I'll remind you: {reminder}"
            return "What would you like me to remind you about?"
        
        # Check for reminders list
        if "reminders" in command:
            reminders = self.memory.get_reminders()
            if reminders:
                return f"You have {len(reminders)} reminders. Check the console."
            return "You have no reminders."
        
        # Process through skills
        result = self.skills.process(command)
        if result:
            return result
        
        return None
    
    def _get_help(self):
        """Return help message"""
        return """I can help you with:

TIME - Get current time
DATE - Get today's date
BATTERY - Check battery level
CPU - Check CPU usage
SEARCH [query] - Search Google
OPEN NOTEPAD - Open Notepad
OPEN CALCULATOR - Open Calculator
OPEN CHROME - Open Chrome
OPEN YOUTUBE - Open YouTube
VOLUME UP/DOWN - Change volume
MUTE - Toggle mute
REMIND [message] - Set a reminder
REMINDERS - Show all reminders
SHUTDOWN - Shutdown computer
HELP - Show this message
EXIT - Quit EDITH

Just type your command!"""