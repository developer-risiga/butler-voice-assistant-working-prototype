import asyncio
import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import logging
import threading
import time

class VoiceEngine:
    """Production-ready voice processing engine"""
    
    def __init__(self):
        self.config = None
        self.logger = logging.getLogger("butler.voice")
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.pygame_initialized = False
        self.is_initialized = False
        self.is_listening = False
        self.wake_word = "butler"
        
    async def initialize(self, config):
        """Initialize voice components"""
        self.config = config
        self.logger.info("Initializing production voice engine...")
        
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
            self.logger.info("✅ Production voice engine initialized!")
            return True
            
        except Exception as e:
            self.logger.error(f"Voice engine init failed: {e}")
            return False
    
    async def wait_for_wake_word(self):
        """Wait for wake word before listening to commands"""
        print(f"🔍 Waiting for wake word: '{self.wake_word}'...")
        
        while True:
            try:
                with self.microphone as source:
                    print("💤 Sleeping... say 'Butler' to wake me up")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                
                # Convert to text
                text = self.recognizer.recognize_google(audio).lower()
                
                if self.wake_word in text:
                    print("🎯 Wake word detected!")
                    await self.speak("Yes? How can I help you?")
                    return True
                    
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                self.logger.debug(f"Wake word listening: {e}")
                continue
    
    async def listen_command(self) -> str:
        """Listen for a voice command after wake word"""
        try:
            print("🎤 Listening for command... (Speak now)")
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=8)
            
            # Convert speech to text
            text = self.recognizer.recognize_google(audio)
            
            if text:
                print(f"🎯 Command: {text}")
                return text
            return ""
            
        except sr.WaitTimeoutError:
            print("⏰ No command detected")
            return ""
        except sr.UnknownValueError:
            print("❌ Could not understand command")
            return ""
        except Exception as e:
            print(f"❌ Command listening error: {e}")
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

print("Production VoiceEngine with wake word defined")
