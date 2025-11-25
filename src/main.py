#!/usr/bin/env python3
from utils.safe_logging import configure_logging
configure_logging()

"""
Butler Voice Assistant - Enhanced Production Version
"""
import os
import sys
import asyncio
import importlib.util
import time
from typing import Dict
import logging
import io


print("🚀 Butler Voice Assistant - Enhanced Production Mode")

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

# Import enhanced production components
from voice.voice_engine import VoiceEngine
from nlu.nlu_engine import NLUEngine
from services.service_manager import ServiceManager
from services.recommendation_engine import RecommendationEngine
from conversation.memory_manager import MemoryManager
from conversation.dialog_manager import DialogManager
from utils.logger import setup_logging
from utils.feedback_manager import FeedbackManager
from ai.thinking_engine import ThinkingEngine
from ai.response_generator import AdaptiveResponseGenerator
from utils.performance_optimizer import PerformanceOptimizer

class UnicodeSafeStreamHandler(logging.StreamHandler):
    """Custom stream handler that safely handles Unicode characters on Windows"""
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            # Encode to UTF-8 and replace any problematic characters
            if sys.platform == "win32":
                msg = msg.encode('utf-8', 'replace').decode('utf-8')
            stream.write(msg + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

def setup_unicode_safe_logging():
    """Setup logging that works with Unicode characters on all platforms"""
    root_logger = logging.getLogger()
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create Unicode-safe handler
    handler = UnicodeSafeStreamHandler(sys.stdout)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Add handler to root logger
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
    
    return root_logger

def fix_unicode_encoding():
    """Fix Unicode encoding issues on Windows"""
    if sys.platform == "win32":
        try:
            # Set stdout and stderr to use UTF-8 encoding
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
            
            # Try to set console code page to UTF-8 on Windows
            os.system('chcp 65001 > nul 2>&1')
        except Exception as e:
            print(f"⚠️ Unicode encoding fix partially applied: {e}")

class EnhancedProductionButler:
    def __init__(self):
        self.config = config
        self.voice_engine = VoiceEngine()
        self.nlu_engine = NLUEngine()
        self.service_manager = ServiceManager()
        self.recommendation_engine = RecommendationEngine()
        self.memory_manager = MemoryManager(config)
        self.dialog_manager = DialogManager()
        self.feedback_manager = FeedbackManager(config)
        self.thinking_engine = ThinkingEngine()
        self.response_generator = AdaptiveResponseGenerator()
        self.performance_optimizer = PerformanceOptimizer(config)
        self.is_running = False
        self.current_mode = "production"  # "production" or "demo"
        self.logger = setup_unicode_safe_logging()
        
    async def initialize(self):
        """Initialize all enhanced production components"""
        print("🔄 Initializing enhanced production Butler...")
        
        try:
            # Apply Unicode fixes
            fix_unicode_encoding()
            
            # Setup safe logging
            setup_unicode_safe_logging()
            
            # Initialize components
            voice_ok = await self.voice_engine.initialize(self.config)
            nlu_ok = await self.nlu_engine.initialize()
            service_ok = await self.service_manager.initialize()
            memory_ok = await self.memory_manager.initialize()
            recommendation_ok = await self.recommendation_engine.initialize()
            feedback_ok = await self.feedback_manager.initialize()
            thinking_ok = await self.thinking_engine.initialize()
            response_ok = await self.response_generator.initialize()
            performance_ok = await self.performance_optimizer.initialize()
            
            # Use text-based logging for initialization status
            if all([voice_ok, nlu_ok, service_ok, memory_ok, recommendation_ok, feedback_ok, thinking_ok, response_ok, performance_ok]):
                print(">>> All enhanced production components initialized!")
                return True
            else:
                print("*** Some components had issues, but continuing...")
                return True
                
        except Exception as e:
            print(f"!!! Enhanced production initialization error: {e}")
            return False
    
    async def start_enhanced_production_mode(self):
        """Start enhanced production interaction loop"""
        self.is_running = True
        self.current_mode = "production"
        
        print("\n" + "="*60)
        print(">>> BUTLER VOICE ASSISTANT - ENHANCED PRODUCTION MODE")
        print("="*60)
        print("*** Enhanced Features:")
        print("   - Multi-step conversations")
        print("   - Smart vendor recommendations") 
        print("   - Vendor comparisons & detailed info")
        print("   - Conversation memory & context")
        print("   - User feedback collection")
        print("="*60)
        print(">>> Say 'Butler' to activate, then your command")
        print(">>> Say 'demo mode' for feature showcase")
        print(">>> Say 'goodbye' or press Ctrl+C to exit")
        print("="*60)
        
        await self.safe_speak("Enhanced Butler is ready! Say Butler to begin, or demo mode for a feature showcase.")
        
        while self.is_running:
            try:
                # Wait for wake word
                wake_detected = await self.voice_engine.wait_for_wake_word()
                
                if wake_detected:
                    # Get command after wake word
                    user_text = await self.voice_engine.listen_command()
                    
                    if not user_text:
                        continue
                        
                    user_text_lower = user_text.lower()
                    
                    # Handle mode switching
                    if 'demo mode' in user_text_lower or 'show me features' in user_text_lower:
                        await self.start_demo_mode()
                        continue
                    elif user_text_lower in ['goodbye', 'bye', 'exit', 'quit']:
                        await self.safe_speak("Goodbye! Thank you for using Butler.")
                        break
                    elif 'feedback' in user_text_lower:
                        await self.handle_feedback_request(user_text)
                    else:
                        await self.process_enhanced_command(user_text)
                    
            except KeyboardInterrupt:
                print("\n*** Stopping Enhanced Butler...")
                break
            except Exception as e:
                print(f"!!! Enhanced production error: {e}")
                await asyncio.sleep(1)
    
    async def process_enhanced_command(self, user_text: str):
        """Process command with real AI thinking"""
        try:
            print(f"👤 You: {user_text}")
            
            # START PERFORMANCE MONITORING
            start_time = time.time()
            
            # Get current context
            context = await self.memory_manager.get_context()
            session_id = context['session']['session_id']
            
            # AI THINKING PROCESS
            thinking_result = await self.thinking_engine.process_thinking(user_text, context)
            print(f">>> Thinking: {thinking_result['thinking_process']}")
            
            # GENERATE THINKING FEEDBACK
            thinking_feedback = await self.response_generator.generate_thinking_feedback(thinking_result)
            await self.safe_speak(thinking_feedback)
            
            # Continue with existing logic but with AI-enhanced responses
            dialog_context = await self.dialog_manager.get_dialog_context(session_id)
            
            if dialog_context and not dialog_context.get('completed', True):
                await self.continue_ai_dialog(session_id, user_text, thinking_result)
            else:
                await self.start_ai_conversation(session_id, user_text, context, thinking_result)
            
            # RECORD PERFORMANCE METRICS
            response_time = time.time() - start_time
            await self.performance_optimizer.record_interaction(
                response_time, user_text, "AI response generated"
            )
            
            # PERFORMANCE FEEDBACK
            if await self.performance_optimizer.should_simplify_responses():
                self.logger.info("*** Performance mode: simplifying responses")
                    
        except Exception as e:
            print(f"!!! AI command processing error: {e}")
            await self.safe_speak("I'm having trouble processing that. Let me try again.")

    async def continue_ai_dialog(self, session_id: str, user_input: str, thinking_result: Dict):
        """Continue dialog with AI thinking"""
        dialog_result = await self.dialog_manager.process_user_response(session_id, user_input)
        
        if dialog_result.get('completed'):
            context = dialog_result['context']
            
            # AI-ENHANCED RESPONSE
            service_data = {'service_type': context.get('service_type', 'service')}
            ai_response = await self.response_generator.generate_adaptive_response(
                thinking_result, service_data, context
            )
            
            await self.safe_speak(ai_response)
        else:
            await self.safe_speak(dialog_result['next_prompt'])
    
    async def start_ai_conversation(self, session_id: str, user_text: str, context: Dict, thinking_result: Dict):
        """Start a new AI-enhanced conversation"""
        # Understand the intent
        nlu_result = await self.nlu_engine.parse(user_text)
        intent = nlu_result['intent']
        entities = nlu_result['entities']
        
        print(f">>> Intent: {intent}")
        print(f">>> Entities: {entities}")
        print(f">>> Context: {context['session']}")
        
        # AI-ENHANCED RESPONSE GENERATION
        service_data = {'service_type': entities.get('service_type', 'service')}
        ai_response = await self.response_generator.generate_adaptive_response(
            thinking_result, service_data, context
        )
        
        # Execute based on intent with enhanced features
        if intent == "find_service":
            response = await self.handle_enhanced_find_service(entities, context)
        elif intent == "book_service":
            # Start booking dialog flow
            await self.dialog_manager.start_dialog(session_id, 'booking_flow', entities)
            next_prompt = await self.dialog_manager.get_next_prompt(session_id)
            response = next_prompt
        elif intent == "greet":
            response = "Hello! I'm your enhanced Butler. I can help you find services, compare vendors, and get smart recommendations. What would you like to do?"
        elif intent == "thanks":
            response = "You're welcome! Would you like to provide feedback on your experience?"
        elif "compare" in user_text.lower():
            response = await self.handle_vendor_comparison(entities, context)
        elif "recommend" in user_text.lower() or "suggest" in user_text.lower():
            response = await self.handle_smart_recommendations(entities, context)
        elif "detail" in user_text.lower() or "info" in user_text.lower():
            response = await self.handle_vendor_details(entities, context)
        else:
            response = "I can help you find services, compare vendors, get recommendations, or book appointments. What would you like to do?"
        
        # Use AI response if available, otherwise use default response
        final_response = ai_response if ai_response else response
        
        # Speak response
        await self.safe_speak(final_response)
        
        # Update conversation memory
        await self.memory_manager.update_conversation(user_text, final_response, intent, entities)
        
        # Check if session should be restarted
        if await self.memory_manager.should_restart_session():
            await self.memory_manager.restart_session()
    
    async def continue_dialog(self, session_id: str, user_input: str):
        """Continue an active dialog flow"""
        dialog_result = await self.dialog_manager.process_user_response(session_id, user_input)
        
        if dialog_result.get('completed'):
            # Dialog completed, execute the final action
            context = dialog_result['context']
            if dialog_result['context'].get('flow_type') == 'booking_flow':
                response = await self.handle_enhanced_booking(context)
            else:
                response = "Action completed successfully!"
        else:
            # Continue with next prompt
            response = dialog_result['next_prompt']
        
        await self.safe_speak(response)
    
    async def handle_enhanced_find_service(self, entities: Dict, context: Dict) -> str:
        """Handle service discovery with enhanced features"""
        service_type = entities.get('service_type', 'plumber')
        location = entities.get('location', 'Bangalore')
        
        # Find services
        result = await self.service_manager.find_services(service_type, location)
        
        # Get smart recommendations
        recommendations = await self.recommendation_engine.get_recommendations(service_type, context)
        
        # Build enhanced response
        response = f"Found {len(result['vendors'])} {service_type} services in {location}. "
        
        if result['vendors']:
            best_vendor = result['vendors'][0]
            response += f"My top recommendation is {best_vendor['name']} with {best_vendor['rating']} stars. "
            
            # Add recommendation insights
            if recommendations:
                rec_vendor = recommendations[0]
                response += f"They have {rec_vendor['experience']} experience and {rec_vendor['reviews']} reviews. "
            
            response += "You can say 'compare vendors', 'get more details', or 'book the first one'."
        
        return response
    
    async def handle_enhanced_booking(self, booking_context: Dict) -> str:
        """Handle enhanced booking with all collected information"""
        service_type = booking_context.get('service_type', 'service')
        datetime = booking_context.get('datetime', 'soon')
        phone = booking_context.get('phone', 'your number')
        
        # Simulate booking
        result = await self.service_manager.book_service(0, {'service_type': service_type})
        
        enhanced_response = f"Booking confirmed! {result['response_text']} "
        enhanced_response += f"Service: {service_type}, Time: {datetime}, Contact: {phone}. "
        enhanced_response += "Thank you for choosing Butler!"
        
        return enhanced_response
    
    async def handle_vendor_comparison(self, entities: Dict, context: Dict) -> str:
        """Handle vendor comparison feature"""
        service_type = entities.get('service_type', 'plumber')
        
        # Get comparison data
        comparison = await self.service_manager.compare_vendors([1, 2, 3])
        
        response = f"Comparing top {service_type} vendors: "
        for i, vendor in enumerate(comparison['vendors'], 1):
            response += f"{i}. {vendor['name']} - {vendor['rating']} stars, {vendor['response_time']} response, {vendor['price_range']}. "
        
        response += "Which one would you like to know more about?"
        
        return response
    
    async def handle_smart_recommendations(self, entities: Dict, context: Dict) -> str:
        """Handle smart recommendations"""
        service_type = entities.get('service_type', 'plumber')
        
        recommendations = await self.recommendation_engine.get_recommendations(service_type, context)
        
        response = f"Based on your needs, here are my top recommendations for {service_type}s: "
        
        for i, rec in enumerate(recommendations, 1):
            response += f"{i}. {rec['name']} - {rec['rating']} stars, {rec['experience']} experience, {rec['response_time']} response. "
        
        return response
    
    async def handle_vendor_details(self, entities: Dict, context: Dict) -> str:
        """Handle detailed vendor information"""
        vendor_id = 1  # Default to first vendor
        vendor_details = await self.service_manager.get_vendor_details(vendor_id)
        
        if vendor_details:
            response = f"Detailed information for {vendor_details['name']}: "
            response += f"Rating: {vendor_details['rating']} stars, "
            response += f"Experience: {vendor_details['experience']}, "
            response += f"Specialization: {vendor_details['specialization']}, "
            response += f"Services: {', '.join(vendor_details['services'])}, "
            response += f"Availability: {vendor_details['availability']}."
        else:
            response = "I couldn't find detailed vendor information at the moment."
        
        return response
    
    async def handle_feedback_request(self, user_text: str):
        """Handle user feedback requests"""
        if 'rate' in user_text.lower() or 'feedback' in user_text.lower():
            await self.safe_speak("I'd love to hear your feedback! On a scale of 1 to 5, how would you rate your experience with Butler?")
            rating_text = await self.voice_engine.listen_command()
            
            try:
                rating = int(''.join(filter(str.isdigit, rating_text)))
                if 1 <= rating <= 5:
                    await self.safe_speak("Thank you! Any additional comments?")
                    comment = await self.voice_engine.listen_command()
                    
                    await self.feedback_manager.record_feedback(
                        "demo_session", rating, comment or "No comment"
                    )
                    
                    stats = await self.feedback_manager.get_feedback_stats()
                    await self.safe_speak(f"Feedback recorded! Our average rating is {stats['average_rating']} stars. Thank you!")
                else:
                    await self.safe_speak("Please provide a rating between 1 and 5.")
            except:
                await self.safe_speak("I didn't catch that rating. Please try again.")
    
    async def start_demo_mode(self):
        """Start interactive demo mode"""
        self.current_mode = "demo"
        
        print("\n" + "="*60)
        print(">>> BUTLER ENHANCED FEATURES DEMO")
        print("="*60)
        
        await self.safe_speak("Welcome to Butler demo mode! I'll showcase all our advanced features.")
        
        # Demo multi-step booking
        await self.safe_speak("First, let me demonstrate our smart multi-step booking process.")
        await asyncio.sleep(1)
        
        demo_steps = [
            "Instead of just booking, I'll guide you through each step:",
            "I'll ask what service you need and your preferred time.",
            "Then I'll get your contact information securely.",
            "Finally, I'll confirm all details before booking."
        ]
        
        for step in demo_steps:
            await self.safe_speak(step)
            await asyncio.sleep(2)
        
        # Demo vendor comparison
        await self.safe_speak("Now, let me show you our vendor comparison feature.")
        await asyncio.sleep(1)
        
        comparison_demo = [
            "I can compare multiple vendors side by side.",
            "You'll see ratings, response times, prices, and experience.",
            "This helps you choose the best provider for your needs.",
            "You can ask for detailed information about any vendor."
        ]
        
        for demo in comparison_demo:
            await self.safe_speak(demo)
            await asyncio.sleep(2)
        
        # Demo smart recommendations
        await self.safe_speak("Finally, let me demonstrate our smart recommendation engine.")
        await asyncio.sleep(1)
        
        recommendation_demo = [
            "I analyze vendor ratings, experience, and customer reviews.",
            "I consider response times and service specialties.",
            "The more you use Butler, the better my recommendations become.",
            "I learn your preferences to suggest perfect matches."
        ]
        
        for demo in recommendation_demo:
            await self.safe_speak(demo)
            await asyncio.sleep(2)
        
        await self.safe_speak("Demo completed! Would you like to try any of these features, or should I return to normal mode?")
        
        # Return to production mode
        self.current_mode = "production"
    
    async def safe_speak(self, text: str):
        """Safely speak text with error handling"""
        try:
            await self.voice_engine.speak(text)
        except Exception as e:
            print(f">>> Butler: {text} (TTS Error: {e})")
    
    async def shutdown(self):
        """Clean shutdown"""
        self.is_running = False
        
        # Show feedback stats
        stats = await self.feedback_manager.get_feedback_stats()
        if stats['total_feedback'] > 0:
            print(f">>> Session Summary: {stats['total_feedback']} feedback entries, Average rating: {stats['average_rating']}/5")
        
        await self.service_manager.shutdown()
        await self.safe_speak("Enhanced Butler is shutting down. Thank you for using our advanced features!")
        print("\n*** Enhanced Production Butler shutdown complete")

async def main():
    """Main entry point"""
    butler = EnhancedProductionButler()
    
    try:
        # Initialize
        success = await butler.initialize()
        if not success:
            print("!!! Enhanced Butler initialization failed!")
            return
        
        # Start enhanced production mode
        await butler.start_enhanced_production_mode()
        
    except Exception as e:
        print(f">>> Enhanced Butler crashed: {e}")
    finally:
        await butler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
