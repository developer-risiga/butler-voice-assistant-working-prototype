#!/usr/bin/env python3
"""
Butler Voice Assistant - Production Ready Version
"""
import os
import sys
import asyncio
import importlib.util

print("🚀 Butler Voice Assistant - Production Mode")

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

# Import production components
from voice.voice_engine import VoiceEngine
from nlu.nlu_engine import NLUEngine
from services.service_manager import ServiceManager
from conversation.memory_manager import MemoryManager
from utils.logger import setup_logging

class ProductionButler:
    def __init__(self):
        self.config = config
        self.voice_engine = VoiceEngine()
        self.nlu_engine = NLUEngine()
        self.service_manager = ServiceManager()
        self.memory_manager = MemoryManager(config)
        self.is_running = False
        
    async def initialize(self):
        """Initialize all production components"""
        print("🔄 Initializing production Butler...")
        
        try:
            # Setup logging
            setup_logging()
            
            # Initialize components
            voice_ok = await self.voice_engine.initialize(self.config)
            nlu_ok = await self.nlu_engine.initialize()
            service_ok = await self.service_manager.initialize()
            memory_ok = await self.memory_manager.initialize()
            
            if all([voice_ok, nlu_ok, service_ok, memory_ok]):
                print("✅ All production components initialized!")
                return True
            else:
                print("⚠️ Some components had issues, but continuing...")
                return True
                
        except Exception as e:
            print(f"❌ Production initialization error: {e}")
            return False
    
    async def start_production_mode(self):
        """Start production interaction loop"""
        self.is_running = True
        
        print("\n" + "="*50)
        print("🏭 BUTLER VOICE ASSISTANT - PRODUCTION MODE")
        print("="*50)
        print("💡 Say 'Butler' to activate, then your command")
        print("📋 Available services: plumbers, electricians, carpenters, etc.")
        print("⏹️  Say 'goodbye' or press Ctrl+C to exit")
        print("="*50)
        
        await self.safe_speak("Butler is ready. Say Butler to get my attention.")
        
        while self.is_running:
            try:
                # Wait for wake word
                wake_detected = await self.voice_engine.wait_for_wake_word()
                
                if wake_detected:
                    # Get command after wake word
                    user_text = await self.voice_engine.listen_command()
                    
                    if user_text and user_text.lower() not in ['goodbye', 'bye', 'exit']:
                        await self.process_production_command(user_text)
                    else:
                        await self.safe_speak("Goodbye! Have a great day!")
                        break
                    
            except KeyboardInterrupt:
                print("\n🛑 Stopping Butler...")
                break
            except Exception as e:
                print(f"❌ Production error: {e}")
                await asyncio.sleep(1)
    
    async def process_production_command(self, user_text: str):
        """Process a command with memory and context"""
        try:
            print(f"👤 You: {user_text}")
            
            # Get current context
            context = await self.memory_manager.get_context()
            
            # Understand the intent
            nlu_result = await self.nlu_engine.parse(user_text)
            intent = nlu_result['intent']
            entities = nlu_result['entities']
            
            print(f"🧠 Intent: {intent}")
            print(f"📊 Entities: {entities}")
            print(f"💾 Context: {context['session']['current_service']}")
            
            # Execute based on intent
            if intent == "find_service":
                response = await self.handle_find_service(entities, context)
            elif intent == "book_service":
                response = await self.handle_book_service(entities, context)
            elif intent == "greet":
                response = "Hello! How can I assist you today?"
            elif intent == "thanks":
                response = "You're welcome! Is there anything else I can help with?"
            else:
                response = "I can help you find local services. What do you need?"
            
            # Speak response
            await self.safe_speak(response)
            
            # Update conversation memory
            await self.memory_manager.update_conversation(user_text, response, intent, entities)
            
            # Check if session should be restarted
            if await self.memory_manager.should_restart_session():
                await self.memory_manager.restart_session()
                await self.safe_speak("Starting fresh conversation. How can I help you?")
                
        except Exception as e:
            print(f"❌ Command processing error: {e}")
            await self.safe_speak("Sorry, I encountered an error. Please try again.")
    
    async def safe_speak(self, text: str):
        """Safely speak text with error handling"""
        try:
            await self.voice_engine.speak(text)
        except:
            print(f"🔊 Butler: {text}")
    
    async def handle_find_service(self, entities: Dict, context: Dict) -> str:
        """Handle service discovery with context"""
        service_type = entities.get('service_type', 'plumber')
        location = entities.get('location', 'Bangalore')
        
        # Find services
        result = await self.service_manager.find_services(service_type, location)
        
        # Build detailed response
        response = f"Found {len(result['vendors'])} {service_type} services in {location}. "
        
        if result['vendors']:
            best_vendor = result['vendors'][0]
            response += f"The top rated is {best_vendor['name']} with {best_vendor['rating']} stars. "
            response += f"You can say 'book the first one' to make a booking."
        
        return response
    
    async def handle_book_service(self, entities: Dict, context: Dict) -> str:
        """Handle service booking with context"""
        service_type = entities.get('service_type', 'service')
        
        # Simulate booking
        result = await self.service_manager.book_service(0, {'service_type': service_type})
        
        return result['response_text']
    
    async def shutdown(self):
        """Clean shutdown"""
        self.is_running = False
        await self.service_manager.shutdown()
        await self.safe_speak("Butler is shutting down. Goodbye!")
        print("\n🔚 Production Butler shutdown complete")

async def main():
    """Main entry point"""
    butler = ProductionButler()
    
    try:
        # Initialize
        success = await butler.initialize()
        if not success:
            print("❌ Production Butler initialization failed!")
            return
        
        # Start production mode
        await butler.start_production_mode()
        
    except Exception as e:
        print(f"💥 Production Butler crashed: {e}")
    finally:
        await butler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
