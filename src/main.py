#!/usr/bin/env python3
"""
Butler Voice Assistant - Stable Working Version
"""
import os
import sys
import asyncio
import importlib.util

print("🚀 Butler Voice Assistant - Starting...")

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

print(f"✅ {config.APP_NAME} v{config.VERSION}")

# Import other components
from voice.voice_engine import VoiceEngine
from nlu.nlu_engine import NLUEngine
from services.service_manager import ServiceManager
from utils.logger import setup_logging

class WorkingButler:
    def __init__(self):
        self.config = config
        self.voice_engine = VoiceEngine()
        self.nlu_engine = NLUEngine()
        self.service_manager = ServiceManager()
        self.is_running = False
        
    async def initialize(self):
        """Initialize all components"""
        print("🔄 Initializing Butler components...")
        
        try:
            # Setup logging
            setup_logging()
            
            # Initialize components
            voice_ok = await self.voice_engine.initialize(self.config)
            nlu_ok = await self.nlu_engine.initialize()
            service_ok = await self.service_manager.initialize()
            
            if voice_ok and nlu_ok and service_ok:
                print("✅ All components initialized successfully!")
                return True
            else:
                print("⚠️ Some components had issues, but continuing...")
                return True
                
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            return False
    
    async def start_interaction(self):
        """Start interaction loop"""
        self.is_running = True
        
        print("\n" + "="*50)
        print("🤖 BUTLER VOICE ASSISTANT - READY")
        print("="*50)
        print("💡 Available commands:")
        print("   - 'hello' or 'hi'")
        print("   - 'find plumbers' or 'need electrician'")
        print("   - 'book service' or 'make appointment'")
        print("   - 'quit' to exit")
        print("="*50)
        
        # Greeting
        await self.safe_speak("Hello! I'm Butler. How can I help you today?")
        
        while self.is_running:
            try:
                # Try voice input first
                user_text = await self.voice_engine.listen()
                
                # If no voice input, use text input as fallback
                if not user_text:
                    user_text = input("\n👤 Type your command (or 'quit'): ").strip()
                
                if user_text.lower() in ['quit', 'exit', 'bye']:
                    break
                    
                if user_text:
                    await self.process_command(user_text)
                    
            except KeyboardInterrupt:
                print("\n🛑 Stopping Butler...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    async def safe_speak(self, text: str):
        """Safely speak text with error handling"""
        try:
            await self.voice_engine.speak(text)
        except:
            print(f"🔊 Butler: {text}")
    
    async def process_command(self, user_text: str):
        """Process a command"""
        try:
            print(f"👤 You: {user_text}")
            
            # Understand the intent
            nlu_result = await self.nlu_engine.parse(user_text)
            intent = nlu_result['intent']
            print(f"🧠 Intent: {intent}")
            
            # Execute based on intent
            if intent == "find_service":
                await self.handle_find_service()
            elif intent == "book_service":
                await self.handle_book_service()
            elif intent == "greet":
                await self.safe_speak("Hello! How can I assist you today?")
            else:
                await self.safe_speak("I can help you find local services like plumbers or electricians. What do you need?")
                
        except Exception as e:
            print(f"❌ Command processing error: {e}")
            await self.safe_speak("Sorry, I encountered an error. Please try again.")
    
    async def handle_find_service(self):
        """Handle service discovery"""
        await self.safe_speak("Looking for plumber services in Bangalore...")
        
        # Find services
        result = await self.service_manager.find_services("plumber", "Bangalore")
        await self.safe_speak(result['response_text'])
        
        # Show results
        if result['vendors']:
            print("\n📋 Found services:")
            for i, vendor in enumerate(result['vendors'], 1):
                print(f"   {i}. {vendor['name']} - Rating: {vendor['rating']}★")
    
    async def handle_book_service(self):
        """Handle service booking"""
        await self.safe_speak("I'll help you book a service. Let me check availability...")
        
        # Simulate booking
        result = await self.service_manager.book_service(0, {})
        await self.safe_speak(result['response_text'])
        
        print(f"📅 Booking ID: {result['booking_id']}")
    
    async def shutdown(self):
        """Clean shutdown"""
        self.is_running = False
        await self.safe_speak("Goodbye! Have a great day!")
        print("\n🔚 Butler shutdown complete")

async def main():
    """Main entry point"""
    butler = WorkingButler()
    
    try:
        # Initialize
        success = await butler.initialize()
        if not success:
            print("❌ Butler initialization failed!")
            return
        
        # Start interaction
        await butler.start_interaction()
        
    except Exception as e:
        print(f"💥 Butler crashed: {e}")
    finally:
        await butler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
