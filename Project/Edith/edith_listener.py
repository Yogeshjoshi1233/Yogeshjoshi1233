import speech_recognition as sr
import queue
import time
import threading
import logging

logger = logging.getLogger(__name__)

class EdithListener:
    """Always-on listener with hotword detection"""
    
    def __init__(self, hotword="edith"):
        self.hotword = hotword.lower()
        self.recognizer = sr.Recognizer()
        
        # Try to get the default microphone
        try:
            self.microphone = sr.Microphone()
            logger.info("Default microphone found")
        except Exception as e:
            logger.error(f"Microphone error: {e}")
            self.microphone = None
        
        self.audio_queue = queue.Queue()
        self.is_listening = False
        
        # Calibrate microphone
        if self.microphone:
            try:
                with self.microphone as source:
                    logger.info("Calibrating microphone...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    logger.info("Microphone calibrated")
            except Exception as e:
                logger.error(f"Calibration error: {e}")
        
        # Start background audio capture
        if self.microphone:
            self._start_audio_capture()
        else:
            logger.error("No microphone available!")
    
    def _start_audio_capture(self):
        """Background thread to capture audio continuously"""
        def capture():
            while True:
                try:
                    if not self.microphone:
                        time.sleep(1)
                        continue
                    
                    with self.microphone as source:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                        self.audio_queue.put(audio)
                except sr.WaitTimeoutError:
                    pass
                except Exception as e:
                    logger.error(f"Audio capture error: {e}")
                    time.sleep(1)
        
        thread = threading.Thread(target=capture, daemon=True)
        thread.start()
        self.is_listening = True
        logger.info("Audio capture started")
    
    def listen(self, timeout=5):
        """Listen for a command with timeout"""
        if not self.microphone:
            logger.error("No microphone available!")
            return None
            
        try:
            audio = self.audio_queue.get(timeout=timeout)
            if not audio:
                return None
                
            text = self.recognizer.recognize_google(audio).lower()
            logger.info(f"Raw text: '{text}'")
            
            # Check for hotword
            if self.hotword in text:
                text = text.replace(self.hotword, "").strip()
                if text:
                    return text
            elif not self.hotword:  # Always listen if no hotword
                return text
            
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            logger.warning(f"Google Speech API error: {e}")
        except queue.Empty:
            pass
        except Exception as e:
            logger.error(f"Listen error: {e}")
        
        return None