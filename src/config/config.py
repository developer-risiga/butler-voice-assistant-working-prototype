import os

class Config:
    """Configuration management for Butler"""
    
    def __init__(self):
        # Application
        self.APP_NAME = "Butler Voice Assistant"
        self.VERSION = "1.0.0"
        self.DEBUG = True
        
        # Voice Settings
        self.WAKE_WORD = "butler"
        self.AUDIO_SAMPLE_RATE = 16000
        self.AUDIO_CHUNK_SIZE = 1024
        self.MAX_RECORDING_SECONDS = 8

        # New : Add conversation timing settings
        self.SLEEP_BETWEEN_CONVERSATIONS = 2  # 2 seconds instead of 300
        self.LISTENING_TIMEOUT = 10  # How long to wait for user speech
        self.WAKE_WORD_TIMEOUT = 5   # How often to check for wake word
       
        # Service Settings
        self.DEFAULT_LOCATION = "Bangalore"
        self.MAX_VENDORS_TO_SHOW = 5
        self.CACHE_DURATION = 30

        # openAI API Configuration
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.OPENAI_MODEL = "gpt-3.5-turbo"
        self.USE_OPENAI = True
        
        # Hardware
        self.LED_PIN = 18
        self.BUTTON_PIN = 17
        
        # Paths
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.MODEL_DIR = os.path.join(self.BASE_DIR, "models")
        self.DATA_DIR = os.path.join(self.BASE_DIR, "data")
        self.CACHE_DIR = os.path.join(self.DATA_DIR, "cache")
        self.LOG_DIR = os.path.join(self.DATA_DIR, "logs")
        self.AUDIO_CACHE_DIR = os.path.join(self.CACHE_DIR, "audio")
        
        # Create directories if they don't exist
        os.makedirs(self.MODEL_DIR, exist_ok=True)
        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.makedirs(self.CACHE_DIR, exist_ok=True)
        os.makedirs(self.LOG_DIR, exist_ok=True)
        os.makedirs(self.AUDIO_CACHE_DIR, exist_ok=True)
    
    @property
    def database_url(self):
        return f"sqlite:///{os.path.join(self.DATA_DIR, 'butler.db')}"
    
    def validate(self):
        """Validate configuration"""
        print("✅ Config validation passed")
        return True

print("Config class initialized")



