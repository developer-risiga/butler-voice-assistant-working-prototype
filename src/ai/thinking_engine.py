import asyncio
import random
import time
from typing import Dict, Any, List
import logging

class ThinkingEngine:
    """AI thinking engine that simulates real-time reasoning"""
    
    def __init__(self):
        self.logger = logging.getLogger("butler.thinking")
        self.conversation_context = {}
        self.user_profile = {}
        self.decision_history = []
        
    async def initialize(self):
        self.logger.info("[THINK] Thinking engine initialized")
        return True
    
    async def process_thinking(self, user_input: str, context: Dict) -> Dict[str, Any]:
        """Main thinking process that analyzes and reasons in real-time"""
        print("💭 Butler is thinking...")
        await asyncio.sleep(0.5)  # Simulate thinking time
        
        # Analyze user intent and emotional state
        analysis = await self._analyze_conversation(user_input, context)
        
        # Generate intelligent response strategy
        strategy = await self._generate_response_strategy(analysis, context)
        
        # Update user profile based on interaction
        await self._update_user_profile(user_input, analysis)
        
        return {
            'analysis': analysis,
            'strategy': strategy,
            'confidence': analysis.get('confidence', 0.8),
            'thinking_process': self._get_thinking_explanation(analysis, strategy)
        }
    
    async def _analyze_conversation(self, user_input: str, context: Dict) -> Dict[str, Any]:
        """Deep analysis of user input and context"""
        input_lower = user_input.lower()
        
        # Emotional analysis
        emotional_state = self._detect_emotional_state(input_lower)
        
        # Urgency detection
        urgency_level = self._detect_urgency(input_lower)
        
        # User expertise level
        expertise_level = self._assess_user_expertise(input_lower, context)
        
        # Context awareness
        context_awareness = self._analyze_context(context)
        
        return {
            'emotional_state': emotional_state,
            'urgency_level': urgency_level,
            'user_expertise': expertise_level,
            'context_awareness': context_awareness,
            'confidence': self._calculate_confidence(input_lower, context),
            'key_entities': self._extract_key_entities(input_lower),
            'conversation_flow': self._analyze_conversation_flow(context)
        }
    
    def _detect_emotional_state(self, text: str) -> str:
        """Detect user's emotional state from text"""
        positive_words = ['thanks', 'thank you', 'great', 'good', 'perfect', 'awesome', 'helpful']
        negative_words = ['urgent', 'emergency', 'problem', 'issue', 'broken', 'not working', 'angry']
        stressed_words = ['asap', 'immediately', 'now', 'quick', 'fast', 'emergency']
        
        if any(word in text for word in stressed_words):
            return "stressed"
        elif any(word in text for word in negative_words):
            return "concerned"
        elif any(word in text for word in positive_words):
            return "satisfied"
        else:
            return "neutral"
    
    def _detect_urgency(self, text: str) -> int:
        """Detect urgency level (1-5)"""
        urgent_indicators = [
            ('emergency', 5), ('urgent', 4), ('asap', 5), ('immediately', 4),
            ('now', 3), ('quick', 3), ('fast', 2), ('soon', 2)
        ]
        
        for indicator, score in urgent_indicators:
            if indicator in text:
                return score
        return 1  # Default non-urgent
    
    def _assess_user_expertise(self, text: str, context: Dict) -> str:
        """Assess user's technical expertise level"""
        technical_terms = ['voltage', 'wiring', 'pipe', 'circuit', 'installation', 'repair']
        simple_terms = ['fix', 'broken', 'not working', 'problem']
        
        tech_count = sum(1 for term in technical_terms if term in text)
        simple_count = sum(1 for term in simple_terms if term in text)
        
        if tech_count > 2:
            return "expert"
        elif tech_count > 0:
            return "intermediate"
        else:
            return "beginner"
    
    def _analyze_context(self, context: Dict) -> Dict[str, Any]:
        """Analyze conversation context for intelligent responses"""
        session = context.get('session', {})
        history = context.get('recent_history', [])
        
        # Detect if this is a follow-up question
        is_follow_up = len(history) > 0
        
        # Detect user's preferred service types
        preferred_services = self._detect_preferences(history)
        
        # Detect conversation pattern
        conversation_pattern = self._detect_conversation_pattern(history)
        
        return {
            'is_follow_up': is_follow_up,
            'preferred_services': preferred_services,
            'conversation_pattern': conversation_pattern,
            'session_duration': time.time() - session.get('start_time', time.time()),
            'interaction_count': len(history)
        }
    
    def _detect_preferences(self, history: List) -> List[str]:
        """Detect user's service preferences from history"""
        services = []
        for interaction in history[-5:]:  # Last 5 interactions
            entities = interaction.get('entities', {})
            if 'service_type' in entities:
                services.append(entities['service_type'])
        return list(set(services))
    
    def _detect_conversation_pattern(self, history: List) -> str:
        """Detect conversation pattern for adaptive responses"""
        if len(history) < 2:
            return "initial"
        
        intents = [h.get('intent') for h in history[-3:]]
        
        if intents.count('find_service') >= 2:
            return "researching"
        elif intents.count('book_service') >= 1:
            return "ready_to_book"
        elif 'greet' in intents and 'find_service' in intents:
            return "standard_flow"
        else:
            return "exploratory"
    
    async def _generate_response_strategy(self, analysis: Dict, context: Dict) -> Dict[str, Any]:
        """Generate intelligent response strategy based on analysis"""
        emotional_state = analysis['emotional_state']
        urgency_level = analysis['urgency_level']
        user_expertise = analysis['user_expertise']
        context_awareness = analysis['context_awareness']
        
        strategy = {
            'tone': self._determine_tone(emotional_state, urgency_level),
            'detail_level': self._determine_detail_level(user_expertise, context_awareness),
            'response_speed': 'immediate' if urgency_level >= 4 else 'normal',
            'suggestions': await self._generate_smart_suggestions(analysis, context),
            'follow_up_questions': self._generate_follow_up_questions(analysis, context)
        }
        
        return strategy
    
    def _determine_tone(self, emotional_state: str, urgency: int) -> str:
        """Determine appropriate tone for response"""
        if emotional_state == "stressed" or urgency >= 4:
            return "reassuring_calm"
        elif emotional_state == "concerned":
            return "empathetic_helpful"
        elif emotional_state == "satisfied":
            return "friendly_positive"
        else:
            return "professional_friendly"
    
    def _determine_detail_level(self, expertise: str, context: Dict) -> str:
        """Determine appropriate level of technical detail"""
        if expertise == "expert":
            return "technical_detailed"
        elif expertise == "intermediate":
            return "balanced"
        else:
            return "simple_explanatory"
    
    async def _generate_smart_suggestions(self, analysis: Dict, context: Dict) -> List[str]:
        """Generate context-aware smart suggestions"""
        suggestions = []
        
        if analysis['urgency_level'] >= 4:
            suggestions.append("emergency_services")
        
        if analysis['context_awareness']['is_follow_up']:
            suggestions.append("related_services")
        
        if analysis['user_expertise'] == "beginner":
            suggestions.append("basic_explanations")
        
        # Add personalized suggestions based on preferences
        preferred_services = analysis['context_awareness']['preferred_services']
        if preferred_services:
            suggestions.append(f"preferred_{preferred_services[0]}_vendors")
        
        return suggestions
    
    def _generate_follow_up_questions(self, analysis: Dict, context: Dict) -> List[str]:
        """Generate intelligent follow-up questions"""
        questions = []
        
        if analysis['context_awareness']['conversation_pattern'] == "researching":
            questions.append("Would you like me to compare the top options?")
            questions.append("Do you need more details about any specific vendor?")
        
        elif analysis['context_awareness']['conversation_pattern'] == "ready_to_book":
            questions.append("Shall I proceed with booking the top-rated vendor?")
            questions.append("Do you have a preferred time for the service?")
        
        return questions
    
    def _get_thinking_explanation(self, analysis: Dict, strategy: Dict) -> str:
        """Generate explanation of the thinking process (for debugging)"""
        return f"Detected {analysis['emotional_state']} emotion, {analysis['urgency_level']} urgency. Using {strategy['tone']} tone with {strategy['detail_level']} details."
    
    async def _update_user_profile(self, user_input: str, analysis: Dict):
        """Update user profile based on interaction"""
        # Simulate learning user preferences
        if 'user_id' not in self.user_profile:
            self.user_profile['user_id'] = 'default_user'
        
        self.user_profile.setdefault('interaction_count', 0)
        self.user_profile['interaction_count'] += 1
        
        # Learn preferred service types
        entities = analysis.get('key_entities', {})
        if 'service_type' in entities:
            self.user_profile.setdefault('preferred_services', [])
            if entities['service_type'] not in self.user_profile['preferred_services']:
                self.user_profile['preferred_services'].append(entities['service_type'])
        
        # Learn communication style preference
        self.user_profile['expertise_level'] = analysis['user_expertise']
        
        self.logger.info(f"📚 Updated user profile: {self.user_profile}")

print("[THINK] ThinkingEngine class defined")


