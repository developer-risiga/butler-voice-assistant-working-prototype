# voice_engine_fixed_logging.py
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
    print("[OK] ElevenLabs imports successful")
except Exception as e:
    print(f"[ERROR] ElevenLabs imports failed: {e}")
    ELEVENLABS_AVAILABLE = False

def configure_logging():
    """
    Configure logging in a safe way for Windows consoles:
      - Reconfigure sys.stdout to utf-8 with errors='replace' (avoids creating wrappers).
      - Attach a StreamHandler that writes to the real sys.stdout.
    """
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # Try to set stdout encoding to utf-8 (Python 3.7+). This does not replace or close sys.stdout.
    try:
        # Reconfigure will modify the existing TextIOBase in-place (safe)
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        # Older Python / unusual streams: ignore and continue
        pass

    # Create a single stream handler that writes to sys.stdout
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(logging.INFO)
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    handler.setFormatter(logging.Formatter(fmt))

    # Remove any existing handlers and add our safe handler
    root.handlers = []
    root.addHandler(handler)

# configure logging early
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
            "butler_default": "VR6AewLTigWG4xSOukaG",
            "butler_premium": "21m00Tcm4TlvDq8ikWAM",
            "professional": "pNInz6obpgDQGcFmaJg"
        }
        self.current_voice = "butler_default"
        self.monthly_char_count = 0
        self.char_limit = 10000  # Free tier example

    async def initialize(self, config=None):
        self.config = config
        self.logger.info("[SYNC] Initializing production voice engine...")

        try:
            # Setup microphone
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

            # Initialize pygame for audio playback (used by Google TTS fallback)
            if not self.pygame_initialized:
                pygame.mixer.init()
                self.pygame_initialized = True

            # Initialize ElevenLabs if available and API key present
            if self.use_elevenlabs:
                success = await self._initialize_elevenlabs()
                if success:
                    self.logger.info("Voice Status: ElevenLabs ENABLED")
                else:
                    self.logger.info("Voice Status: ElevenLabs DISABLED - Using Google TTS")
            else:
                if not ELEVENLABS_AVAILABLE:
                    self.logger.info("Voice Status: ElevenLabs SDK not installed - Using Google TTS")
                else:
                    self.logger.info("Voice Status: ElevenLabs API key missing - Using Google TTS")

            self.is_initialized = True
            self.logger.info("[OK] Production voice engine initialized!")
            return True

        except Exception as e:
            self.logger.exception(f"[ERROR] Voice engine init failed: {e}")
            return False

    async def _initialize_elevenlabs(self):
        try:
            if not ELEVENLABS_AVAILABLE or not self.elevenlabs_api_key:
                return False

            self.elevenlabs_client = ElevenLabs(api_key=self.elevenlabs_api_key)

            try:
                voices_resp = self.elevenlabs_client.voices.search()
                n_voices = len(getattr(voices_resp, "voices", []))
                self.logger.info(f"[OK] ElevenLabs initialized with {n_voices} voices available!")
            except Exception as inner_e:
                self.logger.warning(f"ElevenLabs voice listing failed: {inner_e}")
                self.use_elevenlabs = False
                self.elevenlabs_client = None
                return False

            return True

        except Exception as e:
            self.logger.exception(f"[ERROR] ElevenLabs initialization failed: {e}")
            self.use_elevenlabs = False
            self.elevenlabs_client = None
            return False

    async def wait_for_wake_word(self):
        self.logger.info(f"[LISTEN] Waiting for wake word: '{self.wake_word}'...")
        while True:
            try:
                with self.microphone as source:
                    self.logger.info("[SLEEP] Sleeping... say 'Butler' to wake me up")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)

                text = self.recognizer.recognize_google(audio).lower()
                if self.wake_word in text:
                    self.logger.info("[TARGET] Wake word detected!")
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
        try:
            self.logger.info("[MIC] Listening for command... (Speak now)")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=8)
            text = self.recognizer.recognize_google(audio)
            if text:
                self.logger.info(f"[TARGET] Command: {text}")
                return text
            return ""
        except sr.WaitTimeoutError:
            self.logger.info("[TIMEOUT] No command detected")
            return ""
        except sr.UnknownValueError:
            self.logger.warning("[ERROR] Could not understand command")
            return ""
        except Exception as e:
            self.logger.exception(f"[ERROR] Command listening error: {e}")
            return ""

    async def speak(self, text: str):
        if text is None:
            return
        if not self.is_initialized:
            # use logger instead of print in critical flows
            self.logger.info(f"Butler (not initialized): {text}")
            return
        try:
            self.logger.info(f"[VOICE] Butler: {text}")
            if self.use_elevenlabs and self.elevenlabs_client:
                if self.monthly_char_count + len(text) <= self.char_limit:
                    await self._speak_elevenlabs(text)
                else:
                    self.logger.warning("ElevenLabs char limit reached; using Google TTS")
                    await self._speak_google_tts(text)
            else:
                await self._speak_google_tts(text)
        except Exception as e:
            self.logger.exception(f"[ERROR] Text-to-speech error: {e}")
            self.logger.info(f"Butler (text only): {text}")

    async def _speak_elevenlabs(self, text: str):
        try:
            audio = self.elevenlabs_client.text_to_speech.convert(
                voice_id=self.voice_profiles.get(self.current_voice),
                text=text,
                model_id="eleven_monolingual_v1",
                voice_settings={"stability": 0.3, "similarity_boost": 0.8}
            )
            play(audio)
            self.monthly_char_count += len(text)
            self.logger.info(f"ElevenLabs used: {len(text)} chars")
        except Exception as e:
            self.logger.exception(f"ElevenLabs TTS failed: {e}")
            await self._speak_google_tts(text)

    async def _speak_google_tts(self, text: str):
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                temp_path = tmp.name
                tts.write_to_fp(tmp)
                tmp.flush()

            if not self.pygame_initialized:
                pygame.mixer.init()
                self.pygame_initialized = True

            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            try:
                os.remove(temp_path)
            except Exception:
                self.logger.debug(f"Could not remove temp file: {temp_path}")
        except Exception as e:
            self.logger.exception(f"Google TTS error: {e}")

    def set_voice_style(self, style: str = "butler_default"):
        if style in self.voice_profiles:
            self.current_voice = style
            self.logger.info(f"Voice style changed to: {style}")
        else:
            self.logger.warning(f"Voice style '{style}' not found, using default")

    def get_voice_status(self):
        return {
            "using_elevenlabs": self.use_elevenlabs,
            "current_voice": self.current_voice,
            "characters_used": self.monthly_char_count,
            "characters_remaining": self.char_limit - self.monthly_char_count,
            "elevenlabs_configured": bool(self.elevenlabs_client)
        }

# quick demo
async def main_demo():
    engine = VoiceEngine()
    ok = await engine.initialize()
    if ok:
        await engine.speak("Hello. This test should play audio.")
    else:
        engine.logger.error("[ERROR] Engine failed to initialize.")

if __name__ == "__main__":
    asyncio.run(main_demo())
