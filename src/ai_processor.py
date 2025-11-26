import openai
import logging
import os
import sys

# Add the config directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.join(current_dir, "config")
sys.path.insert(0, config_dir)

# Import Config the same way as in main.py
import importlib.util
config_path = os.path.join(config_dir, "config.py")
spec = importlib.util.spec_from_file_location("butler_config", config_path)
config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config_module)
Config = config_module.Config

class AIProcessor:
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger("butler.ai")
        self.client = None
        self.setup_openai()
    
    def setup_openai(self):
        if self.config.OPENAI_API_KEY:
            openai.api_key = self.config.OPENAI_API_KEY
            self.client = openai.OpenAI()
            self.logger.info("✅ OpenAI ready")
        else:
            self.logger.warning("❌ OpenAI API key not found")
    
    async def process_query(self, user_input):
        if not self.client:
            return "I'm sorry, my AI features are currently unavailable."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Butler, a helpful voice assistant. Be concise and conversational in your responses. Answer in 1-2 sentences maximum."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=100
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            return "I encountered an error processing your request."
