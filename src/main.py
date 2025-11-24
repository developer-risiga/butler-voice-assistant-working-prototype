#!/usr/bin/env python3
"""
Butler Voice Assistant - Real-Time Working Device
"""
import os
import sys
import asyncio
import importlib.util

print("🚀 Butler Voice Assistant - Real-Time Mode")

# Import all components
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import Config
config_path = os.path.join(current_dir, "config", "config.py")
spec = importlib.util.spec_from_file_location("butler_config", config_path)
config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config_module)
Config = config_module.Config
config = Config()

# Import other components
from voice.voice_engine import VoiceEngine
from nlu.nlu_engine import NLUEngine
from services.service_manager import ServiceManager
from utils.logger import setup_logging

class RealTimeButler:
    def __init__(self):
        self.config = config
        self.voice_engine = VoiceEngine()
        self.nlu_engine = NLUEngine()
        self.service_manager = ServiceManager()
        self.is_running = False
        
    async def initialize(self):
        """Initialize all components for real-time use"""
        print("🔄 Initializing real-time Butler...")
        
        # Setup logging
        setup_logging()
        
        # Initialize components
        await self.voice_engine.initialize(self.config)
        await self.nlu_engine.initialize()
        await self.service_manager.initialize()
        
        print("✅ Real-time Butler initialized!")
        return True
    
    async def start_voice_interaction(self):
        """Start voice interaction loop"""
        self.is_running = True
        
        print("\n" + "="*50)
        print("🎧 BUTLER VOICE ASSISTANT - REAL TIME")
        print("="*50)
        print("💡 Say: 'Hello Butler', 'Find plumbers', or 'Book service'")
        print("⏹️  Press Ctrl+C to stop")
        print("="*50)
        
        # Initial greeting
        await self.voice_engine.speak("Hello! I'm Butler. I'm ready to help you.")
        
        while self.is_running:
            try:
                # Listen for voice input
                user_text = await self.voice_engine.listen()
                
                if user_text and len(user_text.strip()) > 2:
                    # Process the command
                    await self.process_command(user_text)
                else:
                    print("💤 Waiting for voice command...")
                    
                await asyncio.sleep(1)
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping Butler...")
                self.is_running = False
            except Exception as e:
                print(f"❌ Error: {e}")
                await asyncio.sleep(1)
    
    async def process_command(self, user_text: str):
        """Process a voice command"""
        try:
            print(f"\n👤 You said: {user_text}")
            
            # Understand the intent
            nlu_result = await self.nlu_engine.parse(user_text)
            intent = nlu_result['intent']
            print(f"🧠 Intent detected: {intent}")
            
            # Execute based on intent
            if intent == "find_service":
                await self.handle_find_service()
            elif intent == "book_service":
                await self.handle_book_service()
            elif intent == "greet":
                await self.voice_engine.speak("Hello! How can I assist you today?")
            else:
                await self.voice_engine.speak("I can help you find local services like plumbers or electricians. Just tell me what you need!")
                
        except Exception as e:
            print(f"❌ Command processing error: {e}")
            await self.voice_engine.speak("Sorry, I didn't understand that. Please try again.")
    
    async def handle_find_service(self):
        """Handle service discovery"""
        await self.voice_engine.speak("Looking for plumber services in Bangalore...")
        
        # Find services
        result = await self.service_manager.find_services("plumber", "Bangalore")
        await self.voice_engine.speak(result['response_text'])
        
        # Offer booking
        await self.voice_engine.speak("You can say 'Book the first one' to make a booking.")
    
    async def handle_book_service(self):
        """Handle service booking"""
        await self.voice_engine.speak("Booking the service for you...")
        
        # Simulate booking
        result = await self.service_manager.book_service(0, {})
        await self.voice_engine.speak(result['response_text'])
    
    async def shutdown(self):
        """Clean shutdown"""
        self.is_running = False
        await self.voice_engine.speak("Goodbye!")
        print("🔚 Butler shutdown complete")

async def main():
    """Main entry point"""
    butler = RealTimeButler()
    
    try:
        # Initialize
        success = await butler.initialize()
        if not success:
            print("❌ Initialization failed!")
            return
        
        # Start real-time voice interaction
        await butler.start_voice_interaction()
        
    except Exception as e:
        print(f"💥 Butler crashed: {e}")
    finally:
        await butler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
