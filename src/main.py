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
        
        # NEW: Import and initialize real conversation engines
        from real_conversation_engine import RealConversationEngine
        from human_response_generator import HumanResponseGenerator
        from real_service_scenarios import RealServiceScenarios
        
        self.real_conversation_engine = RealConversationEngine()
        self.human_response_generator = HumanResponseGenerator()
        self.service_scenarios = RealServiceScenarios()
        self.conversation_history = []
        
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
            
            # NEW: Initialize real conversation components
            conversation_ok = await self.real_conversation_engine.initialize()
            human_response_ok = await self.human_response_generator.initialize()
            scenarios_ok = await self.service_scenarios.initialize()
            
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
        """Start REAL conversation mode (replaces demo mode)"""
        self.is_running = True
        self.current_mode = "production"
        
        print("\n" + "="*60)
        print("🎙️  BUTLER - REAL CONVERSATION MODE")
        print("="*60)
        print("💬 Now speaking like a human assistant")
        print("🛠️  Ready to handle real service requests")
        print("📍 Say 'Butler' then your service need")
        print("⏹️  Say 'goodbye' or press Ctrl+C to exit")
        print("="*60)
        
        # NEW: Real greeting instead of demo announcement
        await self.safe_speak("Hello! I'm Butler, your personal service assistant. I'm ready to help you find reliable service professionals. Just say 'Butler' followed by what you need!")
        
        while self.is_running:
            try:
                # Wait for wake word
                wake_detected = await self.voice_engine.wait_for_wake_word()
                
                if wake_detected:
                    # Get REAL user command
                    user_text = await self.voice_engine.listen_command()
                    
                    if not user_text:
                        continue
                        
                    user_text_lower = user_text.lower()
                    
                    # Handle exit commands
                    if user_text_lower in ['goodbye', 'bye', 'exit', 'quit', 'stop']:
                        await self.safe_speak("Goodbye! Thank you for using Butler. Have a great day!")
                        break
                    elif 'feedback' in user_text_lower:
                        await self.handle_feedback_request(user_text)
                    else:
                        # NEW: Process with REAL conversation engine
                        await self.process_real_conversation(user_text)
                    
            except KeyboardInterrupt:
                self.logger.info("[STOP] Stopping Enhanced Butler...")
                break
            except Exception as e:
                self.logger.error(f"[ERROR] Enhanced production error: {e}")
                await asyncio.sleep(1)
    
    async def process_real_conversation(self, user_text: str):
        """NEW: Process real conversations instead of demo mode"""
        try:
            self.logger.info(f"[USER] You: {user_text}")
            
            # Use REAL conversation engine
            response = await self.real_conversation_engine.process_real_query(user_text)
            
            # Speak natural response
            await self.safe_speak(response)
            
            # Track conversation history
            self.conversation_history.append(user_text)
            self.conversation_history.append(response)
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
                    
        except Exception as e:
            self.logger.error(f"[ERROR] Conversation processing error: {e}")
            await self.safe_speak("I'm having trouble understanding. Could you please repeat that?")

    async def handle_real_service_flow(self, service_type: str, user_input: str):
        """Handle real service conversations"""
        self.logger.info(f"[SERVICE] Handling {service_type} request")
        
        # Ask for details
        detail_prompt = await self.service_scenarios.get_service_details_prompt(service_type)
        await self.safe_speak(detail_prompt)
        
        # Listen for user response
        user_details = await self.voice_engine.listen_command()
        
        if user_details:
            # Ask for timing
            timing_question = await self.service_scenarios.get_timing_question()
            await self.safe_speak(timing_question)
            
            # Listen for timing response
            user_timing = await self.voice_engine.listen_command()
            
            if user_timing:
                # Ask for location
                location_question = await self.service_scenarios.get_location_question()
                await self.safe_speak(location_question)
                
                # Listen for location response
                user_location = await self.voice_engine.listen_command()
                
                if user_location:
                    # Provide realistic next steps
                    confirmation = f"Perfect! I have your {service_type} request for {user_timing} in {user_location}. I'm now searching for available professionals in your area. This may take a moment."
                    await self.safe_speak(confirmation)
                    
                    # Simulate searching (replace with real API later)
                    await asyncio.sleep(2)
                    await self.safe_speak("I've found several qualified professionals available. When we integrate with service APIs, I'll be able to show you their ratings, prices, and book instantly!")

    async def process_enhanced_command(self, user_text: str):
        """Process command with real AI thinking"""
        try:
            self.logger.info(f"[USER] You: {user_text}")
            
            # START PERFORMANCE MONITORING
            start_time = time.time()
            
            # Get current context
            context = await self.memory_manager.get_context()
            session_id = context['session']['session_id']
            
            # AI THINKING PROCESS
            thinking_result = await self.thinking_engine.process_thinking(user_text, context)
            self.logger.info(f"[THINK] Thinking: {thinking_result['thinking_process']}")
            
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
                self.logger.info("[PERF] Performance mode: simplifying responses")
                    
        except Exception as e:
            self.logger.error(f"[ERROR] AI command processing error: {e}")
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
        
        self.logger.info(f"[AI] Intent: {intent}")
        self.logger.info(f"[DATA] Entities: {entities}")
        self.logger.info(f"[MEMORY] Context: {context['session']}")
        
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
    
    async def safe_speak(self, text: str):
        """Safely speak text with error handling"""
        try:
            await self.voice_engine.speak(text)
        except Exception as e:
            self.logger.error(f"[VOICE] Butler: {text} (TTS Error: {e})")
    
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
