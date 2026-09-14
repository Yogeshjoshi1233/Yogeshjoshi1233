import json
from pathlib import Path
from datetime import datetime
import threading
import logging

logger = logging.getLogger(__name__)

class EdithMemory:
    """EDITH's memory and context"""
    
    def __init__(self, memory_file="data/memory.json"):
        self.memory_file = Path(memory_file)
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.lock = threading.Lock()
        self.data = self._load()
        
        # Initialize structure if empty
        if not self.data:
            self.data = {
                "interactions": [],
                "reminders": [],
                "preferences": {}
            }
            self._save()
            logger.info("New memory file created")
        
        logger.info(f"Memory loaded ({len(self.data.get('interactions', []))} interactions)")
    
    def _load(self):
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save(self):
        with self.lock:
            try:
                with open(self.memory_file, 'w') as f:
                    json.dump(self.data, f, indent=2)
            except Exception as e:
                logger.error(f"Failed to save memory: {e}")
    
    def add_interaction(self, command, response):
        """Store every interaction"""
        self.data["interactions"].append({
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "response": response
        })
        
        # Keep only last 1000 to prevent bloat
        if len(self.data["interactions"]) > 1000:
            self.data["interactions"] = self.data["interactions"][-1000:]
        
        self._save()
    
    def add_reminder(self, text):
        """Add a reminder"""
        self.data["reminders"].append({
            "text": text,
            "created": datetime.now().isoformat(),
            "done": False
        })
        self._save()
        logger.info(f"Reminder added: {text}")
    
    def get_reminders(self):
        """Get all active reminders"""
        active = [r for r in self.data["reminders"] if not r["done"]]
        return active
    
    def get_context(self):
        """Get recent conversation context"""
        recent = self.data["interactions"][-5:]
        return recent
    
    def get_preference(self, key, default=None):
        """Get a user preference"""
        return self.data["preferences"].get(key, default)
    
    def set_preference(self, key, value):
        """Set a user preference"""
        self.data["preferences"][key] = value
        self._save()