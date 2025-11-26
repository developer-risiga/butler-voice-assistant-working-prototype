#!/usr/bin/env python3
from utils.safe_logging import configure_logging
configure_logging()

"""
Butler Voice Assistant - REAL-TIME Production Version
"""
import os
import sys
import asyncio
import importlib.util
import time
from typing import Dict
import logging


print("[ROCKET] Butler Voice Assistant - REAL-TIME Production Mode")

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

# NEW: Import real-time conversation engines
from real_conversation_engine import RealConversationEngine
from human_response_generator import HumanResponseGenerator
from real_service_scenarios import RealServiceScenarios

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
        
        # NEW: Real-time conversation engines
        self.real_conversation_engine = RealConversationEngine()
        self.human_response_generator = HumanResponseGenerator()
        self.service_scenarios = RealServiceScenarios()
        
        # NEW: Enhanced session management
        self.conversation_history = []
        self.last_interaction_time = None
        self.session_timeout = 300  # 5 minutes of inactivity
        self.is_awake = False
        self.current_user_id = "default"
        
        # NEW: Real-time booking state
        self.active_booking = None
        self.booking_data = {}
        
    async def initialize(self):
        """Initialize all enhanced production components"""
        self.logger.info("[SYNC] Initializing REAL-TIME production Butler...")
        
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
                self.logger.info("[OK] All REAL-TIME production components initialized!")
                return True
            else:
                self.logger.warning("[WARN] Some components had issues, but continuing...")
                return True
                
        except Exception as e:
            self.logger.error(f"[ERROR] REAL-TIME production initialization error: {e}")
            return False
    
    async def start_enhanced_production_mode(self):
        """REAL-TIME conversation mode with intelligent session management"""
        self.is_running = True
        self.current_mode = "production"
        self.last_interaction_time = time.time()
        
        print("\n" + "="*60)
        print("🎙️  BUTLER - REAL-TIME CONVERSATION MODE")
        print("="*60)
        print("💬 Human-like conversations with context awareness")
        print("📅 Real-time service booking flows")
        print("🚨 Emergency response handling")
        print("⏰ 5-minute active session timeout")
        print("="*60)
        
        await self.safe_speak("Hello! I'm Butler, your real-time service assistant. I can help you book plumbers, electricians, cleaners, carpenters, and more. Just speak naturally and I'll understand!")
        
        while self.is_running:
            try:
                # Check for session timeout
                if self._should_sleep():
                    if self.is_awake:
                        await self.safe_speak("I haven't heard from you in a while. I'm going to sleep now. Just say 'Butler' when you need me again!")
                        self.is_awake = False
                        self._reset_conversation_state()
                
                if not self.is_awake:
                    # Wait for wake word
                    wake_detected = await self.voice_engine.wait_for_wake_word()
                    if wake_detected:
                        self.is_awake = True
                        self.last_interaction_time = time.time()
                        await self.safe_speak("Yes, I'm here! How can I help you today?")
                else:
                    # Listen for command in real-time
                    user_text = await self.voice_engine.listen_command()
                    
                    if user_text:
                        self.last_interaction_time = time.time()  # Reset timer
                        user_text_lower = user_text.lower()
                        
                        # Handle sleep/exit commands
                        if any(word in user_text_lower for word in ['sleep', 'goodbye', 'bye', 'exit', 'stop']):
                            await self.safe_speak("Going to sleep now. Say 'Butler' whenever you need assistance!")
                            self.is_awake = False
                            self._reset_conversation_state()
                        elif 'butler' in user_text_lower:
                            # Reset on wake word even when already awake
                            self.last_interaction_time = time.time()
                            await self.safe_speak("Yes, I'm listening! What can I help you with?")
                        elif 'feedback' in user_text_lower:
                            await self.handle_feedback_request(user_text)
                        else:
                            # Process with REAL-TIME conversation engine
                            await self.process_real_time_conversation(user_text)
                    else:
                        # No speech detected, but stay awake
                        self.logger.info("[ACTIVE] Listening for your command...")
                        
            except KeyboardInterrupt:
                self.logger.info("[STOP] Stopping REAL-TIME Butler...")
                break
            except Exception as e:
                self.logger.error(f"[ERROR] REAL-TIME session error: {e}")
                await asyncio.sleep(1)
    
    def _should_sleep(self) -> bool:
        """Check if Butler should go to sleep due to inactivity"""
        if not self.last_interaction_time:
            return False
        return (time.time() - self.last_interaction_time) > self.session_timeout
    
    def _reset_conversation_state(self):
        """Reset all conversation state when going to sleep"""
        self.active_booking = None
        self.booking_data = {}
        self.human_response_generator.clear_conversation_history(self.current_user_id)
    
  async def process_real_time_conversation(self, user_text: str):
    """REAL-TIME conversation processing with intelligent routing"""
    try:
        self.logger.info(f"[USER] {user_text}")
        
        # Check if user is in an active booking flow
        if self.current_user_id in self.real_conversation_engine.booking_flows:
            self.logger.info(f"[BOOKING] Continuing active booking flow")
            response = await self.real_conversation_engine.process_real_query(user_text, self.current_user_id)
            await self.safe_speak(response)
        else:
            # Use intelligent routing for new conversations
            await self.intelligent_conversation_router(user_text)
        
        # Track conversation for analytics
        self.conversation_history.append({"user": user_text, "butler": "response_given"})
        
        # Keep history manageable
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
                
    except Exception as e:
        self.logger.error(f"[ERROR] REAL-TIME conversation error: {e}")
        await self.safe_speak("I'm having trouble processing that. Let me try again. What service do you need?")

      async def intelligent_conversation_router(self, user_text: str):
        """Intelligently route conversations to the right handler"""
        user_text_lower = user_text.lower()
    
        self.logger.info(f"[ROUTER] Analyzing: {user_text}")
    
        # 1. Emergency detection (highest priority)
        if any(word in user_text_lower for word in ['emergency', 'urgent', 'help now', 'immediately']):
            self.logger.info("[ROUTER] → Emergency handler")
            await self.handle_emergency_request(user_text)
            return
        
        # 2. Service request detection
        service_type = self.real_conversation_engine.extract_service_type(user_text)
        if service_type != "service professional":
            self.logger.info(f"[ROUTER] → Service booking for: {service_type}")
            await self.start_service_booking(user_text, service_type)
            return
        
        # 3. Payment discussions
        if any(word in user_text_lower for word in ['pay', 'payment', 'cost', 'price', 'how much']):
            self.logger.info("[ROUTER] → Payment handler")
            await self.handle_payment_discussion(user_text)
            return
        
        # 4. Capabilities request
        if any(word in user_text_lower for word in ['what can you do', 'capabilities', 'features']):
            self.logger.info("[ROUTER] → Capabilities handler")
            await self.demonstrate_capabilities()
            return
        
        # 5. Default to human conversation
        self.logger.info("[ROUTER] → Default human conversation")
        response = await self.human_response_generator.generate_conversation_response(
            user_text, self.current_user_id
        )
        await self.safe_speak(response)

async def start_service_booking(self, user_text: str, service_type: str):
    """Start a service booking flow"""
    self.logger.info(f"[BOOKING] Starting booking flow for {service_type}")
    
    # Start the booking flow in the real conversation engine
    await self.real_conversation_engine.start_booking_flow(self.current_user_id, service_type)
    
    # Get the initial response for this service
    response = await self.real_conversation_engine.process_real_query(user_text, self.current_user_id)
    await self.safe_speak(response)

    async def handle_service_booking_flow(self, user_text: str):
        """Handle complete service booking flow in real-time"""
        try:
            # Process with real conversation engine
            response = await self.real_conversation_engine.process_real_query(
                user_text, self.current_user_id
            )
            
            await self.safe_speak(response)
            
            # Check if booking was completed
            if "booking confirmed" in response.lower() or "booked" in response.lower():
                self.logger.info("[BOOKING] Service booking completed successfully")
                # Reset booking state
                self.active_booking = None
                self.booking_data = {}
            
        except Exception as e:
            self.logger.error(f"[ERROR] Booking flow error: {e}")
            await self.safe_speak("I encountered an issue with the booking process. Let's try again. What service did you need?")

    async def handle_emergency_request(self, user_text: str):
        """Handle emergency service requests with priority"""
        self.logger.info("[EMERGENCY] Processing emergency request")
        
        # Extract service type from emergency request
        service_type = self.real_conversation_engine.extract_service_type(user_text)
        
        # Get emergency response
        emergency_response = await self.service_scenarios.get_emergency_response(
            service_type, user_text
        )
        
        await self.safe_speak(emergency_response)
        
        # Start emergency booking flow
        await self.real_conversation_engine.start_booking_flow(
            self.current_user_id, service_type
        )

    async def handle_payment_discussion(self, user_text: str):
        """Handle payment-related conversations"""
        payment_responses = [
            "I handle payments securely through multiple options including UPI, cards, and net banking. The exact cost will be confirmed once we select a service professional.",
            "Payments are processed securely. Most services require advance payment confirmation. I'll provide the exact amount when we choose a professional.",
            "I facilitate secure payments for all bookings. Costs vary by service type - I'll give you the final amount before confirming the booking."
        ]
        
        import random
        response = random.choice(payment_responses)
        await self.safe_speak(response)

    async def demonstrate_capabilities(self):
        """Demonstrate what Butler can do"""
        capabilities = (
            "Here's what I can help you with in real-time:\n\n"
            "🔧 SERVICE BOOKING:\n"
            "• Plumbers for leaks, clogs, installations\n"
            "• Electricians for wiring, repairs, installations\n" 
            "• Cleaners for home, office, deep cleaning\n"
            "• Carpenters for furniture, repairs, custom work\n"
            "• AC repair technicians\n\n"
            "🚨 EMERGENCY SERVICES:\n"
            "• Immediate assistance for urgent situations\n"
            "• Priority connection with professionals\n"
            "• Real-time availability checking\n\n"
            "💳 PAYMENT & PRICING:\n"
            "• Cost estimates for all services\n"
            "• Secure payment processing\n"
            "• Transparent pricing\n\n"
            "What would you like to try first?"
        )
        await self.safe_speak(capabilities)

    # NEW: Enhanced service handling methods
    async def process_complete_service_flow(self, service_type: str, user_input: str):
        """Process complete service flow from detection to booking"""
        self.logger.info(f"[SERVICE] Starting {service_type} service flow")
        
        # Step 1: Get problem details
        detail_prompt = await self.service_scenarios.get_service_details_prompt(
            service_type, user_input
        )
        await self.safe_speak(detail_prompt)
        
        # Listen for problem details
        problem_details = await self.voice_engine.listen_command()
        if problem_details:
            self.booking_data['problem'] = problem_details
            
            # Step 2: Get timing
            timing_question = await self.service_scenarios.get_timing_question(service_type)
            await self.safe_speak(timing_question)
            
            timing_response = await self.voice_engine.listen_command()
            if timing_response:
                self.booking_data['timing'] = timing_response
                
                # Step 3: Get location
                location_question = await self.service_scenarios.get_location_question()
                await self.safe_speak(location_question)
                
                location_response = await self.voice_engine.listen_command()
                if location_response:
                    self.booking_data['location'] = location_response
                    self.booking_data['service_type'] = service_type
                    
                    # Step 4: Confirm and book
                    confirmation = await self.service_scenarios.get_booking_confirmation(
                        service_type, self.booking_data
                    )
                    await self.safe_speak(confirmation)
                    
                    # Listen for confirmation
                    confirm_response = await self.voice_engine.listen_command()
                    if confirm_response and ('yes' in confirm_response.lower() or 'confirm' in confirm_response.lower()):
                        await self.safe_speak("Perfect! I'm now searching for available professionals in your area...")
                        
                        # Simulate searching (replace with real API later)
                        await asyncio.sleep(2)
                        
                        # Provide realistic booking result
                        booking_result = (
                            f"🎉 Booking confirmed! I've found available {service_type} professionals "
                            f"for your {self.booking_data.get('problem', 'service')} in {self.booking_data.get('location', 'your area')}. "
                            f"They'll contact you shortly to confirm the timing."
                        )
                        await self.safe_speak(booking_result)
                        
                        # Reset booking data
                        self.booking_data = {}
                    else:
                        await self.safe_speak("No problem! I've cancelled the booking. Let me know if you need anything else.")
                        self.booking_data = {}

    # NEW: Intelligent conversation routing
    async def route_conversation(self, user_text: str):
        """Intelligently route conversations to appropriate handlers"""
        user_text_lower = user_text.lower()
        
        # Emergency detection
        if any(word in user_text_lower for word in ['emergency', 'urgent', 'help now', 'immediately']):
            await self.handle_emergency_request(user_text)
            return
        
        # Payment discussions
        if any(word in user_text_lower for word in ['pay', 'payment', 'cost', 'price', 'how much']):
            await self.handle_payment_discussion(user_text)
            return
        
        # Service type detection
        service_type = self.real_conversation_engine.extract_service_type(user_text)
        if service_type != "service professional":
            await self.start_service_booking(user_text, service_type)
            return
        
        # Capabilities demonstration
        if any(word in user_text_lower for word in ['what can you do', 'capabilities', 'features']):
            await self.demonstrate_capabilities()
            return
        
        # Default to general conversation
        await self.process_real_time_conversation(user_text)

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
                    await self.safe_speak("Thank you! Any additional comments or suggestions?")
                    comment = await self.voice_engine.listen_command()
                    
                    await self.feedback_manager.record_feedback(
                        "real_time_session", rating, comment or "No comment"
                    )
                    
                    stats = await self.feedback_manager.get_feedback_stats()
                    await self.safe_speak(f"Thank you for your {rating}-star rating! Our average is {stats['average_rating']} stars. Your feedback helps me improve!")
                else:
                    await self.safe_speak("Please provide a rating between 1 and 5.")
            except:
                await self.safe_speak("I didn't catch that rating. Let's try again later.")

    async def shutdown(self):
        """Clean shutdown with proper error handling"""
        self.is_running = False
        
        try:
            # Show conversation analytics
            if self.conversation_history:
                self.logger.info(f"[STATS] Session had {len(self.conversation_history)} conversations")
            
            # Show feedback stats
            stats = await self.feedback_manager.get_feedback_stats()
            if stats['total_feedback'] > 0:
                self.logger.info(f"[STATS] Total feedback: {stats['total_feedback']}, Average rating: {stats['average_rating']}/5")
            
            # Shutdown service manager
            await self.service_manager.shutdown()
            
            # Speak shutdown message
            await self.safe_speak("Butler is shutting down. Thank you for using our real-time service assistant!")
            
            self.logger.info("[END] REAL-TIME Butler shutdown complete")
            
        except Exception as e:
            self.logger.error(f"[ERROR] Shutdown error: {e}")
        finally:
            # Ensure we exit cleanly even if there are errors
            await asyncio.sleep(0.1)

async def main():
    """Main entry point"""
    butler = EnhancedProductionButler()
    
    try:
        # Initialize
        success = await butler.initialize()
        if not success:
            print("[ERROR] REAL-TIME Butler initialization failed!")
            return
        
        print("\n" + "="*60)
        print("🚀 BUTLER REAL-TIME MODE ACTIVATED")
        print("="*60)
        print("Ready for human-like conversations!")
        print("Try commands like:")
        print("• 'I need a plumber for a leaking pipe'")
        print("• 'Book an electrician for tomorrow'") 
        print("• 'Emergency - water leaking everywhere!'")
        print("• 'How much does AC repair cost?'")
        print("="*60)
        
        # Start REAL-TIME production mode
        await butler.start_enhanced_production_mode()
        
    except KeyboardInterrupt:
        print("\n[STOP] Received interrupt signal...")
    except Exception as e:
        print(f"[CRASH] REAL-TIME Butler crashed: {e}")
    finally:
        await butler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
