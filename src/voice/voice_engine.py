import asyncio
import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import whisper
import logging

class VoiceEngine:
    """Real voice processing engine"""
    
    def __init__(self):
        self.config = None
        self.logger = logging.getLogger("butler.voice")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.whisper_model = None
        self.is_initialized = False
        
    async def initialize(self, config):
        """Initialize with real voice components"""
        self.config = config
        self.logger.info("Initializing real voice engine...")
        
        try:
            # Setup microphone
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Load Whisper model
            self.logger.info("Loading Whisper model...")
            self.whisper_model = whisper.load_model("base")
            
            # Initialize pygame
            pygame.mixer.init()
            
            self.is_initialized = True
            self.logger.info("✅ Real voice engine initialized!")
            return True
            
        except Exception as e:
            self.logger.error(f"Voice engine init failed: {e}")
            return False
    
    async def listen(self) -> str:
        """Listen for voice input and return text"""
        try:
            print("🎤 Listening... (Speak now)")
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)
            
            # Convert speech to text
            text = await self.speech_to_text(audio)
            return text
            
        except sr.WaitTimeoutError:
            print("⏰ No speech detected")
            return ""
        except Exception as e:
            print(f"❌ Listening error: {e}")
            return ""
    
    async def speech_to_text(self, audio) -> str:
        """Convert speech to text using Whisper"""
        try:
            import numpy as np
            audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
            audio_data = audio_data.astype(np.float32) / 32768.0
            
            result = self.whisper_model.transcribe(audio_data)
            text = result["text"].strip()
            
            if text:
                print(f"🎯 Heard: {text}")
                return text
            return ""
            
        except Exception as e:
            print(f"❌ Speech-to-text error: {e}")
            return ""
    
    async def speak(self, text: str):
        """Convert text to speech and play it"""
        if not text:
            return
            
        try:
            print(f"🔊 Butler: {text}")
            
            # Use Google TTS
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save to buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Play audio
            pygame.mixer.music.load(audio_buffer)
            pygame.mixer.music.play()
            
            # Wait for playback
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
                
        except Exception as e:
            print(f"❌ Text-to-speech error: {e}")
            print(f"Butler (text only): {text}")

print("Real VoiceEngine class defined")
