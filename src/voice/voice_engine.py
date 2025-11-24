import asyncio
import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import logging

class VoiceEngine:
    """Lightweight voice processing engine"""
    
    def __init__(self):
        self.config = None
        self.logger = logging.getLogger("butler.voice")
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.pygame_initialized = False
        self.is_initialized = False
        
    async def initialize(self, config):
        """Initialize voice components"""
        self.config = config
        self.logger.info("Initializing lightweight voice engine...")
        
        try:
            # Setup microphone
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Initialize pygame for audio playback
            if not self.pygame_initialized:
                pygame.mixer.init()
                self.pygame_initialized = True
            
            self.is_initialized = True
            self.logger.info("✅ Lightweight voice engine initialized!")
            return True
            
        except Exception as e:
            self.logger.error(f"Voice engine init failed: {e}")
            return False
    
    async def listen(self) -> str:
        """Listen for voice input and return text"""
        if not self.is_initialized:
            return ""
            
        try:
            print("🎤 Listening... (Speak now)")
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=5)
            
            # Convert speech to text using Google STT (online)
            text = self.recognizer.recognize_google(audio)
            
            if text:
                print(f"🎯 Heard: {text}")
                return text
            return ""
            
        except sr.WaitTimeoutError:
            print("⏰ No speech detected")
            return ""
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return ""
        except Exception as e:
            print(f"❌ Listening error: {e}")
            return ""
    
    async def speak(self, text: str):
        """Convert text to speech and play it"""
        if not text or not self.is_initialized:
            print(f"Butler: {text}")
            return
            
        try:
            print(f"🔊 Butler: {text}")
            
            # Use Google TTS
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save to buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Ensure pygame is initialized
            if not self.pygame_initialized:
                pygame.mixer.init()
                self.pygame_initialized = True
            
            # Play audio
            pygame.mixer.music.load(audio_buffer)
            pygame.mixer.music.play()
            
            # Wait for playback
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
                
        except Exception as e:
            print(f"❌ Text-to-speech error: {e}")
            print(f"Butler (text only): {text}")

print("Lightweight VoiceEngine class defined")
