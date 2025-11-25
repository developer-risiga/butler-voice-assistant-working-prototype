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


print("[ROCKET] Butler Voice Assistant - Enhanced Production Mode")

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

print(f"[OK] {config.APP_NAME} v{config.VERSION}")

# Import enhanced production components
from voice.voice_engine import VoiceEngine
from nlu.nlu_engine import NLUEngine
from services.service_manager import ServiceManager
from services.recommendation_engine import RecommendationEngine
from conversation.memory_manager import MemoryManager
from conversation.dialog_manager import DialogManager
from utils.feedback_manager import FeedbackManager
from ai.thinking_engine import ThinkingEngine
from ai.response_generator import AdaptiveResponseGenerator
from utils.performance_optimizer import PerformanceOptimizer

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
        self.current_mode = "production"
        self.logger = logging.getLogger("butler.main")
        self.conversation_history = []
        
        # NEW: Session management variables
        self.last_interaction_time = None
        self.session_timeout = 300  # 5 minutes of inactivity
        self.is_awake = False
        
        # NEW: Conversation context tracking
        self.current_service_type = None
        self.conversation_context = {}
        
    async def initialize(self):
        """Initialize all enhanced production components"""
        self.logger.info("[SYNC] Initializing enhanced production Butler...")
        
        try:
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
            
            if all([voice_ok, nlu_ok, service_ok, memory_ok, recommendation_ok, feedback_ok, thinking_ok, response_ok, performance_ok]):
                self.logger.info("[OK] All enhanced production components initialized!")
                return True
            else:
                self.logger.warning("[WARN] Some components had issues, but continuing...")
                return True
                
        except Exception as e:
            self.logger.error(f"[ERROR] Enhanced production initialization error: {e}")
            return False
    
    async def start_enhanced_production_mode(self):
        """Enhanced with session management"""
        self.is_running = True
        self.current_mode = "production"
        self.last_interaction_time = time.time()
        
        print("\n" + "="*60)
        print("🎙️  BUTLER - ACTIVE SESSION MODE")
        print("="*60)
        print("💬 I'll stay awake for 5 minutes after each interaction")
        print("🔄 Say 'Butler' anytime to reset the timer")
        print("💤 I'll automatically sleep after 5 minutes of inactivity")
        print("="*60)
        
        await self.safe_speak("Hello! I'm Butler. I'll stay active and ready to help. Just speak naturally!")
        
        while self.is_running:
            try:
                # Check for session timeout
                if (time.time() - self.last_interaction_time) > self.session_timeout:
                    if self.is_awake:
                        await self.safe_speak("I haven't heard from you in a while. I'm going to sleep now. Say 'Butler' when you need me!")
                        self.is_awake = False
                        self._reset_conversation_context()
                
                if not self.is_awake:
                    # Wait for wake word
                    wake_detected = await self.voice_engine.wait_for_wake_word()
                    if wake_detected:
                        self.is_awake = True
                        self.last_interaction_time = time.time()
                        await self.safe_speak("I'm here! How can I help you?")
                else:
                    # Listen for command without timeout parameter
                    user_text = await self.voice_engine.listen_command()
                    
                    if user_text:
                        self.last_interaction_time = time.time()  # Reset timer
                        user_text_lower = user_text.lower()
                        
                        # Handle sleep commands
                        if any(word in user_text_lower for word in ['sleep', 'goodbye', 'bye']):
                            await self.safe_speak("Going to sleep now. Say 'Butler' when you need me!")
                            self.is_awake = False
                            self._reset_conversation_context()
                        elif 'butler' in user_text_lower:
                            # Reset on wake word even when already awake
                            self.last_interaction_time = time.time()
                            await self.safe_speak("Yes, I'm listening!")
                        elif 'feedback' in user_text_lower:
                            await self.handle_feedback_request(user_text)
                        else:
                            await self.process_real_conversation(user_text)
                    else:
                        # No speech detected, but don't sleep immediately
                        self.logger.info("[ACTIVE] No speech detected, but staying awake...")
                        
            except KeyboardInterrupt:
                self.logger.info("[STOP] Stopping Enhanced Butler...")
                break
            except Exception as e:
                self.logger.error(f"[ERROR] Session mode error: {e}")
                await asyncio.sleep(1)
    
    def _reset_conversation_context(self):
        """Reset conversation context when going to sleep"""
        self.current_service_type = None
        self.conversation_context = {}
    
    async def process_real_conversation(self, user_text: str):
        """NEW: Process real conversations with context awareness"""
        try:
            self.logger.info(f"[USER] You: {user_text}")
            
            # Use enhanced conversation engine with context
            response = await self.process_real_query_with_context(user_text)
            
            # Speak natural response
            await self.safe_speak(response)
            
            # Track conversation history
            self.conversation_history.append({"user": user_text, "butler": response})
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
                    
        except Exception as e:
            self.logger.error(f"[ERROR] Conversation processing error: {e}")
            await self.safe_speak("I'm having trouble understanding. Could you please repeat that?")

    async def process_real_query_with_context(self, user_text: str) -> str:
        """Process user queries with context awareness"""
        user_text_lower = user_text.lower()
        
        # Check if we're in the middle of a service conversation
        if self.current_service_type:
            return await self.handle_service_follow_up(user_text, self.current_service_type)
        
        # Service-related queries - SIMPLIFIED LOGIC
        service_type = await self.detect_service_intent_simple(user_text_lower)
        if service_type:
            self.current_service_type = service_type
            self.conversation_context['service_type'] = service_type
            return await self.handle_service_request(user_text, service_type)
        
        # Greetings
        elif any(word in user_text_lower for word in ['hello', 'hi', 'hey']):
            return "Hello there! How can I help you today? I can assist with finding service professionals like plumbers, electricians, or cleaners."
        
        # Help requests
        elif 'help' in user_text_lower:
            return "Of course! I specialize in connecting you with reliable service professionals. You can ask me to find plumbers, electricians, carpenters, cleaners, or other home services. What do you need help with?"
        
        # Thank you
        elif any(word in user_text_lower for word in ['thank', 'thanks']):
            return "You're very welcome! Is there anything else I can help you with today?"
        
        # Default response
        else:
            return "I understand you're looking for assistance. I'm here to help you find reliable service professionals. Could you tell me what kind of service you need?"
    
    async def detect_service_intent_simple(self, user_text_lower: str) -> str:
        """Simplified service intent detection - just look for keywords"""
        service_keywords = {
            'plumber': ['plumb', 'pipe', 'leak', 'drain', 'faucet', 'toilet', 'sink', 'water', 'clog', 'blocked'],
            'electrician': ['electric', 'wiring', 'outlet', 'socket', 'switch', 'power', 'light', 'circuit', 'fan', 'appliance'],
            'cleaner': ['clean', 'cleaning', 'housekeeping', 'maid', 'sanitize', 'dust', 'mop', 'vacuum'],
            'carpenter': ['carpent', 'wood', 'furniture', 'cabinet', 'shelf', 'repair', 'build', 'install']
        }
        
        for service_type, keywords in service_keywords.items():
            for keyword in keywords:
                if keyword in user_text_lower:
                    return service_type
        
        return None

    async def handle_service_follow_up(self, user_text: str, service_type: str) -> str:
        """Handle follow-up questions in service conversations"""
        user_text_lower = user_text.lower()
        
        # Check for specific plumbing issues
        if service_type == 'plumber':
            if any(word in user_text_lower for word in ['leak', 'leaking']):
                return "I understand you have a leak. This sounds urgent! Let me find plumbers who specialize in leak repairs. Could you tell me where the leak is located?"
            elif any(word in user_text_lower for word in ['drain', 'clog', 'blocked', 'slow']):
                return "A clogged drain can be frustrating! I'll find plumbers experienced with drain cleaning. Is this for a kitchen sink, bathroom sink, or shower drain?"
            elif any(word in user_text_lower for word in ['toilet', 'flush']):
                return "Toilet issues need immediate attention! I'll connect you with toilet repair specialists. Is the toilet not flushing properly, running continuously, or leaking?"
            elif any(word in user_text_lower for word in ['faucet', 'tap']):
                return "Faucet problems are common! I'll find experts in faucet repair and replacement. Is it dripping, leaking, or not producing water properly?"
        
        # Generic follow-up for any service
        if not self.conversation_context.get('details_asked'):
            self.conversation_context['details_asked'] = True
            return await self.get_service_details_prompt(service_type)
        elif not self.conversation_context.get('timing_asked'):
            self.conversation_context['timing_asked'] = True
            return await self.get_timing_question()
        elif not self.conversation_context.get('location_asked'):
            self.conversation_context['location_asked'] = True
            location_response = await self.get_location_question()
            # Add context that we're ready to search
            return location_response + " Once I have your location, I can start searching for available professionals."
        else:
            # All information collected, proceed to search
            self._reset_conversation_context()
            return f"Perfect! I have all the details about your {service_type} request. Let me search for available professionals in your area. This might take a moment..."
    
    async def handle_service_request(self, user_text: str, service_type: str) -> str:
        """Handle specific service requests with better context"""
        user_text_lower = user_text.lower()
        
        if service_type == 'plumber':
            # Check for specific plumbing issues in the initial request
            if any(word in user_text_lower for word in ['leak', 'leaking']):
                self.conversation_context['issue_type'] = 'leak'
                return "I understand you have a plumbing leak. This sounds urgent! Let me ask a few questions to find the right plumber. Where is the leak located?"
            elif any(word in user_text_lower for word in ['drain', 'clog', 'blocked', 'slow']):
                self.conversation_context['issue_type'] = 'clogged_drain'
                return "A clogged drain can be frustrating! I'll help you find a drain specialist. Which drain is affected - kitchen, bathroom, or shower?"
            elif any(word in user_text_lower for word in ['toilet', 'flush']):
                self.conversation_context['issue_type'] = 'toilet'
                return "Toilet issues need prompt attention! I'll connect you with toilet repair experts. What exactly is happening with the toilet?"
            else:
                return "I can help you find a reliable plumber! Could you tell me more about what you need? For example, is it a leaky faucet, clogged drain, toilet issue, or something else?"
        
        elif service_type == 'electrician':
            return "I can connect you with qualified electricians! What specific electrical work do you need? Installation, repairs, lighting, or something else?"
        
        elif service_type == 'cleaner':
            return "I know several excellent cleaning services! Are you looking for regular house cleaning, deep cleaning, or office cleaning?"
        
        elif service_type == 'carpenter':
            return "I can help you find skilled carpenters! What type of woodwork do you need? Furniture repair, custom work, or installations?"
        
        else:
            return "I understand you need a service professional. Could you tell me what specifically you need help with? The more details you provide, the better I can assist you."

    async def get_service_details_prompt(self, service_type: str) -> str:
        """Get natural prompt for service details"""
        import random
        
        prompts = {
            'plumber': [
                "Could you describe the plumbing issue you're experiencing? For example, is it a leak, clogged drain, or something else?",
                "What kind of plumbing work do you need help with? The more details you provide, the better I can match you with the right professional.",
                "I know several excellent plumbers with different specialties. Could you tell me what specifically needs to be fixed or installed?"
            ],
            'electrician': [
                "What electrical work are you looking to have done? Installation, repairs, lighting, or something else?",
                "Electrical work can vary quite a bit. Could you describe what you need so I can find the right electrician for the job?",
                "I want to make sure I connect you with an electrician who specializes in your specific need. What exactly requires attention?"
            ],
            'cleaner': [
                "What type of cleaning service are you looking for? Regular maintenance, deep cleaning, move-in/out cleaning, or something specific?",
                "Cleaning needs can vary - are you looking for general house cleaning, office cleaning, or something more specialized?",
                "Could you tell me about the space that needs cleaning and what kind of cleaning service you're expecting?"
            ]
        }
        
        default_prompt = "Could you tell me more about what you need? The details will help me find the perfect service professional for you."
        
        if service_type in prompts:
            return random.choice(prompts[service_type])
        else:
            return f"Could you describe what you need from the {service_type}? This will help me find the right professional for your specific situation."
    
    async def get_timing_question(self) -> str:
        """Get natural timing question"""
        import random
        
        questions = [
            "When would you like the service to be completed? Are you thinking today, this week, or is it more flexible?",
            "What's your preferred timing for this service? Is it urgent, or do you have some flexibility?",
            "When were you hoping to have this work done? This helps me check availability with the professionals."
        ]
        return random.choice(questions)
    
    async def get_location_question(self) -> str:
        """Get natural location question"""
        import random
        
        questions = [
            "Could you tell me your location or area? This helps me find professionals who service your neighborhood.",
            "What area are you located in? I'll search for service providers who cover your location.",
            "Which part of the city are you in? This ensures I only recommend professionals who work in your area."
        ]
        return random.choice(questions)

    async def safe_speak(self, text: str):
        """Safely speak text with error handling"""
        try:
            await self.voice_engine.speak(text)
        except Exception as e:
            self.logger.error(f"[VOICE] Butler: {text} (TTS Error: {e})")

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

    async def shutdown(self):
        """Clean shutdown with proper error handling"""
        self.is_running = False
        
        try:
            # Show feedback stats
            stats = await self.feedback_manager.get_feedback_stats()
            if stats['total_feedback'] > 0:
                self.logger.info(f"[STATS] Session Summary: {stats['total_feedback']} feedback entries, Average rating: {stats['average_rating']}/5")
            
            # Shutdown service manager
            await self.service_manager.shutdown()
            
            # Speak shutdown message
            await self.safe_speak("Enhanced Butler is shutting down. Thank you for using our advanced features!")
            
            self.logger.info("[END] Enhanced Production Butler shutdown complete")
            
        except Exception as e:
            self.logger.error(f"[ERROR] Shutdown error: {e}")
        finally:
            # Ensure we exit cleanly even if there are errors
            await asyncio.sleep(0.1)  # Small delay to ensure all tasks complete

async def main():
    """Main entry point"""
    butler = EnhancedProductionButler()
    
    try:
        # Initialize
        success = await butler.initialize()
        if not success:
            print("[ERROR] Enhanced Butler initialization failed!")
            return
        
        # Start enhanced production mode
        await butler.start_enhanced_production_mode()
        
    except KeyboardInterrupt:
        print("\n[STOP] Received interrupt signal...")
    except Exception as e:
        print(f"[CRASH] Enhanced Butler crashed: {e}")
    finally:
        await butler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
