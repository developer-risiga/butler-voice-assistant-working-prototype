import openai
import logging
import os

class AIProcessor:
    def __init__(self):
        self.logger = logging.getLogger("butler.ai")
        self.client = None
        self.setup_openai()
    
    def setup_openai(self):
        api_key = os.getenv("OPENAI_API_KEY")
        
        if api_key and api_key.startswith("sk-"):
            self.client = openai.OpenAI(api_key=api_key)
            self.logger.info("✅ OpenAI initialized successfully")
        else:
            self.logger.error("❌ Invalid OpenAI API key")
    
    async def process_query(self, user_input):
        if not self.client:
            return "AI service is currently unavailable."
        
        try:
            self.logger.info(f"[AI] Asking: {user_input}")
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}],
                max_tokens=150
            )
            
            answer = response.choices[0].message.content
            self.logger.info(f"[AI] Answer: {answer}")
            return answer
            
        except Exception as e:
            self.logger.error(f"[AI ERROR] {e}")
            return "I apologize, but I'm having trouble accessing information right now. Please try a different question."
