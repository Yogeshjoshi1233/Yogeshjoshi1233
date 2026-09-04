import time
import threading
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EdithBackground:
    """Background tasks like reminders, auto-checks, etc."""
    
    def __init__(self, speaker, memory):
        self.speaker = speaker
        self.memory = memory
        self.running = True
        self.last_reminder_check = 0
        
        logger.info("Background services initialized")
    
    def run(self):
        """Main background loop"""
        logger.info("Background services started")
        
        while self.running:
            try:
                # Check reminders every 30 seconds
                if time.time() - self.last_reminder_check > 30:
                    self._check_reminders()
                    self.last_reminder_check = time.time()
                
                # Check for scheduled tasks
                self._check_scheduled_tasks()
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logger.error(f"Background error: {e}")
                time.sleep(10)
    
    def _check_reminders(self):
        """Check and announce reminders"""
        try:
            reminders = self.memory.check_reminders()
            for reminder in reminders:
                self.speaker.speak(f"Reminder: {reminder}")
                logger.info(f"Reminder announced: {reminder}")
        except Exception as e:
            logger.error(f"Reminder check error: {e}")
    
    def _check_scheduled_tasks(self):
        """Check any scheduled tasks"""
        # Example: Daily greeting at 9 AM
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        if current_time == "09:00":
            if self.memory.get_preference("greeted_today", False) == False:
                self.speaker.speak("Good morning! I'm here to help.")
                self.memory.set_preference("greeted_today", True)
                self._schedule_reset_greeting()
    
    def _schedule_reset_greeting(self):
        """Reset the greeting flag at midnight"""
        def reset():
            while self.running:
                if datetime.now().strftime("%H:%M") == "00:00":
                    self.memory.set_preference("greeted_today", False)
                    break
                time.sleep(60)
        
        thread = threading.Thread(target=reset, daemon=True)
        thread.start()
    
    def stop(self):
        """Stop background services"""
        self.running = False
        logger.info("Background services stopped")