import openai
import logging
import os

class AIProcessor:
    def __init__(self):
        self.logger = logging.getLogger("butler.ai")
        self.client = None
        self.setup_openai()
    
    def setup_openai(self):
        # Get API key directly from environment
        api_key = os.getenv("OPENAI_API_KEY")
        
        if api_key and api_key != "your_actual_openai_api_key_here":
            openai.api_key = api_key
            self.client = openai.OpenAI()
            self.logger.info("✅ OpenAI ready")
            self.logger.info(f"✅ OpenAI API key found: {api_key[:10]}...") 
        else:
            self.logger.error("❌ OpenAI API key not found or is placeholder")
            self.logger.error("❌ Check your .env file for OPENAI_API_KEY")
    
    async def process_query(self, user_input):
        if not self.client:
            error_msg = "I'm sorry, my AI features are currently unavailable."
            self.logger.error("[AI] OpenAI client not available")
            return error_msg
        
        try:
            self.logger.info(f"[AI] Processing query: {user_input}")
            
            # SIMPLIFIED API call with better error handling
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are Butler, a helpful voice assistant. Answer in 2-3 short sentences."
                    },
                    {
                        "role": "user", 
                        "content": user_input
                    }
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            self.logger.info(f"[AI SUCCESS] Response: {ai_response}")
            return ai_response
            
        except Exception as e:
            self.logger.error(f"[AI ERROR] OpenAI API error: {str(e)}")
            return "I apologize, but I'm having trouble accessing my knowledge right now. Please try again in a moment."
