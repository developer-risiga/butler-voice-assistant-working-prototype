# voice_engine_fixed.py
import asyncio
import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import logging
import os
import tempfile
import sys

# ElevenLabs imports with proper error handling
try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs.play import play
    ELEVENLABS_AVAILABLE = True
    print("✅ ElevenLabs imports successful")
except Exception as e:
    print(f"❌ ElevenLabs imports failed: {e}")
    ELEVENLABS_AVAILABLE = False

def configure_logging():
    """Configure logging to avoid UnicodeEncodeError on Windows consoles."""
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # Wrap stdout buffer with utf-8 TextIOWrapper and replace invalid characters
    utf8_stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    handler = logging.StreamHandler(stream=utf8_stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    # remove other handlers and add ours
    if root.handlers:
        for h in list(root.handlers):
            root.removeHandler(h)
    root.addHandler(handler)

# call logger config early
configure_logging()

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
        
        # ElevenLabs Configuration: read API key from env (do NOT hardcode)
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY", "")
        self.use_elevenlabs = ELEVENLABS_AVAILABLE and bool(self.elevenlabs_api_key)
        self.elevenlabs_client = None
        
        # Voice profiles (voice IDs — confirm these in your ElevenLabs console)
        self.voice_profiles = {
            "butler_default": "VR6AewLTigWG4xSOukaG",  # example voice id
            "butler_premium": "21m00Tcm4TlvDq8ikWAM",
            "professional": "pNInz6obpgDQGcFmaJg"
        }
        self.current_voice = "butler_default"
        self.monthly_char_count = 0
        self.char_limit = 10000  # Free tier example
        
    async def initialize(self, config=None):
        """Initialize voice components"""
        self.config = config
        self.logger.info("Initializing production voice engine...")
        
        try:
            # Setup microphone
            self.microphone = sr.Microphone()
            with self.microphone as source:
                # adjust for ambient noise once at startup
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Initialize pygame for audio playback (used by Google TTS fallback)
            if not self.pygame_initialized:
                # init mixer only once
                pygame.mixer.init()
                self.pygame_initialized = True
            
            # Initialize ElevenLabs if available and API key present
            if self.use_elevenlabs:
                success = await self._initialize_elevenlabs()
                if success:
                    self.logger.info("🎯 Voice Status: ElevenLabs ENABLED")
                else:
                    self.logger.info("🎯 Voice Status: ElevenLabs DISABLED - Using Google TTS")
            else:
                if not ELEVENLABS_AVAILABLE:
                    self.logger.info("🎯 Voice Status: ElevenLabs SDK not installed - Using Google TTS")
                else:
                    self.logger.info("🎯 Voice Status: ElevenLabs API key missing - Using Google TTS")
            
            self.is_initialized = True
            self.logger.info("✅ Production voice engine initialized!")
            return True
            
        except Exception as e:
            self.logger.exception(f"❌ Voice engine init failed: {e}")
            return False
    
    async def _initialize_elevenlabs(self):
        """Initialize ElevenLabs client with proper error handling"""
        try:
            if not ELEVENLABS_AVAILABLE or not self.elevenlabs_api_key:
                return False
                
            self.elevenlabs_client = ElevenLabs(api_key=self.elevenlabs_api_key)
            
            # Try a simple voices call to validate the key & connection
            try:
                voices_resp = self.elevenlabs_client.voices.search()
                n_voices = len(getattr(voices_resp, "voices", []))
                self.logger.info(f"✅ ElevenLabs initialized with {n_voices} voices available!")
            except Exception as inner_e:
                self.logger.warning(f"❌ ElevenLabs voice listing failed: {inner_e}")
                self.use_elevenlabs = False
                self.elevenlabs_client = None
                return False
            
            return True
            
        except Exception as e:
            self.logger.exception(f"❌ ElevenLabs initialization failed: {e}")
            self.use_elevenlabs = False
            self.elevenlabs_client = None
            return False
    
    async def wait_for_wake_word(self):
        """Wait for wake word before listening to commands"""
        self.logger.info(f"🔍 Waiting for wake word: '{self.wake_word}'...")
        
        while True:
            try:
                with self.microphone as source:
                    self.logger.info("💤 Sleeping... say 'Butler' to wake me up")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                
                # Convert to text
                text = self.recognizer.recognize_google(audio).lower()
                
                if self.wake_word in text:
                    self.logger.info("🎯 Wake word detected!")
                    await self.speak("Yes? How can I help you?")
                    return True
                    
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                self.logger.debug(f"Wake-word listen error: {e}")
                continue
    
    async def listen_command(self) -> str:
        """Listen for a voice command after wake word"""
        try:
            self.logger.info("🎤 Listening for command... (Speak now)")
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=8)
            
            # Convert speech to text
            text = self.recognizer.recognize_google(audio)
            
            if text:
                self.logger.info(f"🎯 Command: {text}")
                return text
            return ""
            
        except sr.WaitTimeoutError:
            self.logger.info("⏰ No command detected")
            return ""
        except sr.UnknownValueError:
            self.logger.warning("❌ Could not understand command")
            return ""
        except Exception as e:
            self.logger.exception(f"❌ Command listening error: {e}")
            return ""
    
    async def speak(self, text: str):
        """Convert text to speech using ElevenLabs or fallback to Google TTS"""
        if text is None:
            return
        
        # If engine not initialized, just print
        if not self.is_initialized:
            print(f"Butler: {text}")
            return
            
        try:
            self.logger.info(f"🔊 Butler: {text}")
            
            # Use ElevenLabs if available and configured
            if self.use_elevenlabs and self.elevenlabs_client:
                # Check character limit
                if self.monthly_char_count + len(text) <= self.char_limit:
                    await self._speak_elevenlabs(text)
                else:
                    self.logger.warning("⚠️ ElevenLabs character limit reached, using Google TTS")
                    await self._speak_google_tts(text)
            else:
                # Fallback to Google TTS
                await self._speak_google_tts(text)
                
        except Exception as e:
            self.logger.exception(f"❌ Text-to-speech error: {e}")
            # Ultimate fallback - just print text
            print(f"Butler (text only): {text}")
    
    async def _speak_elevenlabs(self, text: str):
        """Use ElevenLabs for high-quality voice generation"""
        try:
            audio = self.elevenlabs_client.text_to_speech.convert(
                voice_id=self.voice_profiles.get(self.current_voice),
                text=text,
                model_id="eleven_monolingual_v1",
                voice_settings={
                    "stability": 0.3,
                    "similarity_boost": 0.8
                }
            )
            
            # Play the audio using the official helper `play`
            play(audio)
            
            # Update character count
            self.monthly_char_count += len(text)
            self.logger.info(f"🎵 ElevenLabs voice used: {len(text)} characters")
            
        except Exception as e:
            self.logger.exception(f"❌ ElevenLabs TTS failed: {e}")
            # Fallback to Google TTS
            await self._speak_google_tts(text)
    
    async def _speak_google_tts(self, text: str):
        """Fallback to Google TTS with reliable Windows playback (temp file)"""
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Write to a temporary file (MP3). On Windows pygame may not accept BytesIO MP3s.
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                temp_path = tmp.name
                # gTTS can write to the file-like object
                tts.write_to_fp(tmp)
                tmp.flush()
            
            # Ensure pygame mixer initialized
            if not self.pygame_initialized:
                pygame.mixer.init()
                self.pygame_initialized = True
            
            # Load and play file
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            # Wait until playback finishes
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            
            # Clean up temp file
            try:
                os.remove(temp_path)
            except Exception:
                self.logger.debug(f"Could not remove temp file: {temp_path}")
                
        except Exception as e:
            self.logger.exception(f"❌ Google TTS error: {e}")
    
    def set_voice_style(self, style: str = "butler_default"):
        """Change the ElevenLabs voice style"""
        if style in self.voice_profiles:
            self.current_voice = style
            self.logger.info(f"🎭 Voice style changed to: {style}")
        else:
            self.logger.warning(f"⚠️ Voice style '{style}' not found, using default")
    
    def get_voice_status(self):
        """Get current voice engine status"""
        return {
            "using_elevenlabs": self.use_elevenlabs,
            "current_voice": self.current_voice,
            "characters_used": self.monthly_char_count,
            "characters_remaining": self.char_limit - self.monthly_char_count,
            "elevenlabs_configured": bool(self.elevenlabs_client)
        }

# Example quick run (for testing)
async def main_demo():
    e = VoiceEngine()
    await e.initialize()
    await e.speak("This is a quick test. Hello from Butler voice assistant.")

if __name__ == "__main__":
    asyncio.run(main_demo())
