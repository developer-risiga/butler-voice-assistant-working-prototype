import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration management for Butler"""
    
    def __init__(self):
        # Application
        self.APP_NAME = "Butler Voice Assistant"
        self.VERSION = "1.0.0"
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        
        # Voice Settings
        self.WAKE_WORD = os.getenv("BUTLER_NAME", "butler").lower()
        self.AUDIO_SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))
        self.AUDIO_CHUNK_SIZE = 1024
        self.MAX_RECORDING_SECONDS = 8
        
        # API Keys
        self.JUSTDIAL_API_KEY = os.getenv("JUSTDIAL_API_KEY", "")
        self.PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY", "")
        self.GOOGLE_STT_API_KEY = os.getenv("GOOGLE_STT_API_KEY", "")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        
        # Service Settings
        self.DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "Bangalore")
        self.MAX_VENDORS_TO_SHOW = int(os.getenv("MAX_VENDORS_TO_SHOW", "5"))
        self.CACHE_DURATION = int(os.getenv("CACHE_DURATION_MINUTES", "30"))
        
        # Hardware
        self.LED_PIN = int(os.getenv("LED_PIN", "18"))
        self.BUTTON_PIN = int(os.getenv("BUTTON_PIN", "17"))
        
        # Paths
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.MODEL_DIR = os.path.join(self.BASE_DIR, "models")
        self.DATA_DIR = os.path.join(self.BASE_DIR, "data")
        
        # Create directories if they don't exist
        os.makedirs(self.MODEL_DIR, exist_ok=True)
        os.makedirs(self.DATA_DIR, exist_ok=True)
    
    @property
    def database_url(self):
        return f"sqlite:///{os.path.join(self.DATA_DIR, 'butler.db')}"
    
    def validate(self):
        """Validate critical configuration"""
        if not self.PORCUPINE_ACCESS_KEY:
            print("Warning: PORCUPINE_ACCESS_KEY not set. Using simulated wake word.")
        if not self.JUSTDIAL_API_KEY:
            print("Warning: JUSTDIAL_API_KEY not set. Using mock data.")
        return True