import logging
import random
from typing import Dict, List
import asyncio

class HumanResponseGenerator:
    """REAL-TIME human-like response generator with conversation memory"""
    
    def __init__(self):
        self.logger = logging.getLogger("butler.response_generator")
        self.conversation_history = {}
        
    async def generate_conversation_response(self, user_input: str, user_id: str = "default") -> str:
        """Generate real-time contextual responses"""
        
        # Initialize conversation history for user
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        history = self.conversation_history[user_id]
        
        # Analyze conversation context
        context_analysis = await self.analyze_conversation_context(user_input, history)
        
        # Generate appropriate response
        if context_analysis['is_follow_up']:
            response = await self.generate_follow_up_response(user_input, context_analysis)
        else:
            response = await self.generate_initial_response(user_input, context_analysis)
        
        # Update conversation history
        history.append({'user': user_input, 'butler': response})
        
        # Keep history manageable (last 5 exchanges)
        if len(history) > 5:
            history = history[-5:]
            self.conversation_history[user_id] = history
        
        return response
    
    async def analyze_conversation_context(self, user_input: str, history: List[Dict]) -> Dict:
        """Analyze conversation context for better responses"""
        
        if not history:
            return {'is_follow_up': False, 'last_topic': None, 'user_intent': 'new'}
        
        last_exchange = history[-1]
        last_butler_message = last_exchange.get('butler', '').lower()
        
        # Detect if this is a follow-up to previous question
        is_follow_up = any(phrase in last_butler_message for phrase in [
            'what specific', 'tell me about', 'describe', 'when would you', 
            'what type of', 'where are you', 'what location'
        ])
        
        # Extract last topic
        last_topic = None
        for topic in ['plumb', 'electric', 'clean', 'carpent', 'ac', 'emergency']:
            if topic in last_butler_message:
                last_topic = topic
                break
        
        return {
            'is_follow_up': is_follow_up,
            'last_topic': last_topic,
            'last_butler_message': last_butler_message,
            'user_intent': 'follow_up' if is_follow_up else 'new'
        }
    
    async def generate_initial_response(self, user_input: str, context: Dict) -> str:
        """Generate initial responses to user input"""
        
        user_input_lower = user_input.lower()
        
        # Enhanced greeting detection
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return await self.generate_greeting_response()
        
        # Service request detection
        elif any(word in user_input_lower for word in ['help', 'need', 'want', 'looking for', 'find', 'book']):
            return await self.generate_service_help_response(user_input)
        
        # Emergency detection
        elif any(word in user_input_lower for word in ['emergency', 'urgent', 'help now', 'immediately']):
            return await self.generate_emergency_response()
        
        # General conversation
        else:
            return await self.generate_general_response()
    
    async def generate_follow_up_response(self, user_input: str, context: Dict) -> str:
        """Generate follow-up responses based on conversation context"""
        
        last_message = context.get('last_butler_message', '')
        
        if 'what specific' in last_message or 'describe' in last_message:
            return await self.acknowledge_details_and_continue(user_input)
        
        elif 'when would you' in last_message or 'timing' in last_message:
            return await self.acknowledge_timing_and_continue(user_input)
        
        elif 'where are you' in last_message or 'location' in last_message:
            return await self.acknowledge_location_and_confirm(user_input)
        
        else:
            return await self.generate_general_follow_up(user_input)
    
    async def generate_greeting_response(self) -> str:
        """Generate natural greeting responses"""
        greetings = [
            "Hello! I'm Butler, your real-time service assistant. I can help you book trusted professionals instantly. What service do you need today?",
            "Hi there! I'm Butler, ready to connect you with reliable service providers in real-time. What can I help you with?",
            "Hello! I'm Butler - here to make service booking effortless. What would you like me to book for you today?"
        ]
        return random.choice(greetings)
    
    async def generate_service_help_response(self, user_input: str) -> str:
        """Generate service assistance responses"""
        help_responses = [
            "I can help you book reliable service professionals! I handle plumbing, electrical work, cleaning, carpentry, AC repair, and more. What specific service do you need?",
            "I'd be happy to assist with service bookings! I work with trusted plumbers, electricians, cleaners, carpenters, and technicians. What are you looking for?",
            "Let me help you find the perfect service professional! I can book various home services instantly. What do you need done?"
        ]
        return random.choice(help_responses)
    
    async def generate_emergency_response(self) -> str:
        """Generate emergency response"""
        emergency_responses = [
            "🚨 Emergency mode activated! I'm prioritizing your request. Please describe the situation and your location for immediate assistance.",
            "🚨 Urgent help is on the way! Tell me what's happening and where you are. I'm finding the nearest available professionals.",
            "🚨 Emergency situation noted! I'm getting you immediate help. What's the emergency and your current location?"
        ]
        return random.choice(emergency_responses)
    
    async def generate_general_response(self) -> str:
        """Generate general conversation responses"""
        general_responses = [
            "I'm here to help you book reliable service professionals in real-time. What type of service are you looking for?",
            "As your service booking assistant, I can connect you with trusted professionals instantly. What do you need help with today?",
            "I specialize in real-time service bookings. I can help with plumbing, electrical work, cleaning, and more. What service can I book for you?"
        ]
        return random.choice(general_responses)
    
    async def acknowledge_details_and_continue(self, user_input: str) -> str:
        """Acknowledge problem details and ask for timing"""
        acknowledgments = [
            "Thanks for explaining! Now, when would you like the service to be done?",
            "I understand the situation better now. What's your preferred timing for this service?",
            "That helps me find the right professional! When should I schedule the service?"
        ]
        return random.choice(acknowledgments)
    
    async def acknowledge_timing_and_continue(self, user_input: str) -> str:
        """Acknowledge timing and ask for location"""
        acknowledgments = [
            "Perfect timing! Now, what's your location? I'll find professionals serving your area.",
            "Great! I've noted the timing. What's your address or area?",
            "Timing confirmed! Now I just need your location to find available professionals nearby."
        ]
        return random.choice(acknowledgments)
    
    async def acknowledge_location_and_confirm(self, user_input: str) -> str:
        """Acknowledge location and provide confirmation"""
        acknowledgments = [
            "Location noted! I have all the details now. Should I proceed with booking and find available professionals?",
            "Perfect! I've got your location. I'm ready to book your service. Should I continue?",
            "Great! With your location, I can now find the best professionals. Ready to book?"
        ]
        return random.choice(acknowledgments)
    
    async def generate_general_follow_up(self, user_input: str) -> str:
        """Generate general follow-up responses"""
        follow_ups = [
            "Thanks for that information! Let's continue with your service booking.",
            "I understand. Let me help you complete your booking.",
            "Got it! I'll use this information to find the right professional for you."
        ]
        return random.choice(follow_ups)
    
    def clear_conversation_history(self, user_id: str = "default"):
        """Clear conversation history for a user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
