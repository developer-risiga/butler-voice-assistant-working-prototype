import openai
import logging
from config import Config

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
    
    async def process_query(self, user_input):
        if not self.client:
            return "AI not available."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Butler, a helpful voice assistant."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=150
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return "I can't process that right now."
