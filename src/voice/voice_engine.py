import asyncio
import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import logging
import threading
import time
import os
from elevenlabs import play
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VoiceEngine:
    """Production-ready voice processing engine with ElevenLabs integration"""
    
    def __init__(self):
        self.config = None
        self.logger = logging.getLogger("butler.voice")
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.pygame_initialized = False
        self.is_initialized = False
        self.is_listening = False
        self.wake_word = "butler"
        
        # ElevenLabs Configuration
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.use_elevenlabs = True if self.elevenlabs_api_key else False
        self.elevenlabs_client = None
        self.voice_profiles = {
            "butler_default": "VR6AewLTigWG4xSOukaG",  # ElevenLabs Josh voice
            "butler_premium": "21m00Tcm4TlvDq8ikWAM",   # Rachel voice
            "professional": "pNInz6obpgDQGcFmaJgB"     # Adam voice
        }
        self.current_voice = "butler_default"
        self.monthly_char_count = 0
        self.char_limit = 10000  # Free tier limit
        
    async def initialize(self, config):
        """Initialize voice components with ElevenLabs"""
        self.config = config
        self.logger.info("Initializing production voice engine with ElevenLabs...")
        
        try:
            # Setup microphone
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Initialize pygame for audio playback (fallback)
            if not self.pygame_initialized:
                pygame.mixer.init()
                self.pygame_initialized = True
            
            # Initialize ElevenLabs client
            if self.use_elevenlabs and self.elevenlabs_api_key:
                try:
                    self.elevenlabs_client = ElevenLabs(api_key=self.elevenlabs_api_key)
                    self.logger.info("✅ ElevenLabs client initialized!")
                    
                    # Test the connection by listing voices
                    voices = self.elevenlabs_client.voices.get_all()
                    self.logger.info(f"🎵 Available ElevenLabs voices: {len(voices.voices)}")
                    
                except Exception as e:
                    self.logger.warning(f"❌ ElevenLabs init failed, using fallback TTS: {e}")
                    self.use_elevenlabs = False
            else:
                self.logger.warning("ElevenLabs API key not found, using Google TTS")
                self.use_elevenlabs = False
            
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
    
    async def speak(self, text: str, use_elevenlabs: bool = None):
        """Convert text to speech using ElevenLabs or fallback to Google TTS"""
        if not text or not self.is_initialized:
            print(f"Butler: {text}")
            return
            
        try:
            print(f"🔊 Butler: {text}")
            
            # Determine if we should use ElevenLabs
            should_use_elevenlabs = use_elevenlabs if use_elevenlabs is not None else self.use_elevenlabs
            
            # Check character limit for ElevenLabs
            if should_use_elevenlabs and self.elevenlabs_client:
                if self.monthly_char_count + len(text) > self.char_limit:
                    self.logger.warning("ElevenLabs character limit reached, using fallback")
                    should_use_elevenlabs = False
            
            # Use ElevenLabs for premium voice
            if should_use_elevenlabs and self.elevenlabs_client:
                await self._speak_elevenlabs(text)
            else:
                # Fallback to Google TTS
                await self._speak_google_tts(text)
                
        except Exception as e:
            print(f"❌ Text-to-speech error: {e}")
            # Ultimate fallback - just print text
            print(f"Butler (text only): {text}")
    
    async def _speak_elevenlabs(self, text: str):
        """Use ElevenLabs for high-quality voice generation"""
        try:
            # Update character count
            self.monthly_char_count += len(text)
            
            # Generate audio with ElevenLabs - CORRECT SYNTAX FOR v2.24.0
            audio = self.elevenlabs_client.text_to_speech.convert(
                voice_id=self.voice_profiles[self.current_voice],
                text=text,
                model_id="eleven_monolingual_v1",
                voice_settings={
                    "stability": 0.3,
                    "similarity_boost": 0.8
                }
            )
            
            # Play the audio - CORRECT SYNTAX
            play(audio)
            
            self.logger.info(f"🎵 ElevenLabs speech: {len(text)} chars (Total: {self.monthly_char_count}/{self.char_limit})")
            
        except Exception as e:
            self.logger.error(f"ElevenLabs TTS failed: {e}")
            # Fallback to Google TTS
            await self._speak_google_tts(text)
    
    async def _speak_google_tts(self, text: str):
        """Fallback to Google TTS"""
        try:
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
            print(f"❌ Google TTS error: {e}")
            raise
    
    def set_voice_style(self, style: str = "butler_default"):
        """Change the ElevenLabs voice style"""
        if style in self.voice_profiles:
            self.current_voice = style
            self.logger.info(f"🎭 Voice style changed to: {style}")
        else:
            self.logger.warning(f"Voice style '{style}' not found, using default")
    
    def update_voice_settings(self, stability: float = 0.3, similarity_boost: float = 0.8):
        """Update ElevenLabs voice settings for emotional control"""
        self.voice_settings = {
            "stability": stability,  # Lower = more emotional/expressive
            "similarity_boost": similarity_boost  # Higher = closer to original voice
        }
    
    def get_usage_stats(self) -> dict:
        """Get ElevenLabs usage statistics"""
        return {
            "characters_used": self.monthly_char_count,
            "character_limit": self.char_limit,
            "remaining_chars": max(0, self.char_limit - self.monthly_char_count),
            "using_elevenlabs": self.use_elevenlabs,
            "current_voice": self.current_voice
        }

print("Enhanced VoiceEngine with ElevenLabs v2.24.0 integration defined")
