import asyncio
from typing import Dict, Any, List
import logging

class AdaptiveResponseGenerator:
    """Generates adaptive, context-aware responses in real-time"""
    
    def __init__(self):
        self.logger = logging.getLogger("butler.response_generator")
        self.response_templates = self._load_response_templates()
        
    async def initialize(self):
        self.logger.info("🎯 Adaptive response generator initialized")
        return True
    
    def _load_response_templates(self) -> Dict[str, Any]:
        """Load comprehensive response templates"""
        return {
            'tones': {
                'reassuring_calm': [
                    "I understand this is urgent. Let me help you quickly find the best solution.",
                    "I can see this needs immediate attention. I'm prioritizing emergency services for you.",
                    "Don't worry, I'll help you resolve this efficiently."
                ],
                'empathetic_helpful': [
                    "I understand your concern. Let me find the most reliable solution for you.",
                    "That sounds frustrating. I'll help you get this sorted out properly.",
                    "I can help with that. Let me find the right experts for your situation."
                ],
                'friendly_positive': [
                    "Great! I'd be happy to help you with that.",
                    "Perfect! Let me find the best options for you.",
                    "Excellent choice! I'll get you connected with top professionals."
                ],
                'professional_friendly': [
                    "I can assist you with that service request.",
                    "Let me help you find the appropriate service providers.",
                    "I'll search for the best available options in your area."
                ]
            },
            
            'detail_levels': {
                'technical_detailed': [
                    "Based on the technical requirements, I recommend vendors with specific expertise in {service_type}.",
                    "Considering the technical nature, I'm filtering for certified professionals with relevant experience.",
                    "For this technical service, I'm prioritizing vendors with proper certifications and specialized equipment."
                ],
                'balanced': [
                    "I'll find experienced {service_type} professionals who can handle your specific needs.",
                    "Let me connect you with reliable {service_type} services that match your requirements.",
                    "I'm searching for qualified {service_type} providers in your area."
                ],
                'simple_explanatory': [
                    "I'll help you find a good {service_type} to fix this for you.",
                    "Let me find someone who can help with your {service_type} needs.",
                    "I'll connect you with a professional who can take care of this for you."
                ]
            },
            
            'urgency_responses': {
                5: "I'm prioritizing emergency services and contacting available professionals immediately.",
                4: "I'll find available professionals who can respond quickly to your urgent request.",
                3: "I'm searching for professionals who can address this in a timely manner.",
                2: "I'll find reliable professionals available for your service needs.",
                1: "I'm compiling the best available options for your consideration."
            },
            
            'follow_up_suggestions': {
                'researching': [
                    "Would you like me to compare the top 3 options side by side?",
                    "Should I provide more details about any specific vendor?",
                    "Would you like to see customer reviews for these providers?"
                ],
                'ready_to_book': [
                    "Shall I proceed with booking the top-rated vendor?",
                    "Would you like me to check availability for your preferred time?",
                    "Should I initiate the booking process with your selected provider?"
                ]
            }
        }
    
    async def generate_adaptive_response(self, thinking_result: Dict, service_data: Dict, context: Dict) -> str:
        """Generate adaptive response based on AI thinking results"""
        strategy = thinking_result['strategy']
        analysis = thinking_result['analysis']
        
        # Build response components
        tone_component = self._get_tone_component(strategy['tone'])
        detail_component = self._get_detail_component(strategy['detail_level'], service_data)
        urgency_component = self._get_urgency_component(analysis['urgency_level'])
        suggestion_component = self._get_suggestion_component(strategy, context)
        
        # Combine components naturally
        response_parts = []
        
        if urgency_component:
            response_parts.append(urgency_component)
        
        response_parts.append(tone_component)
        response_parts.append(detail_component)
        
        if suggestion_component:
            response_parts.append(suggestion_component)
        
        # Add follow-up questions if appropriate
        if strategy['follow_up_questions']:
            response_parts.append(self._select_random(strategy['follow_up_questions']))
        
        # Combine into natural response
        final_response = " ".join(response_parts)
        
        self.logger.info(f"🎯 Generated adaptive response with {strategy['tone']} tone")
        return final_response
    
    def _get_tone_component(self, tone: str) -> str:
        """Get appropriate tone component"""
        return self._select_random(self.response_templates['tones'][tone])
    
    def _get_detail_component(self, detail_level: str, service_data: Dict) -> str:
        """Get appropriate detail level component"""
        template = self._select_random(self.response_templates['detail_levels'][detail_level])
        service_type = service_data.get('service_type', 'service')
        return template.format(service_type=service_type)
    
    def _get_urgency_component(self, urgency_level: int) -> str:
        """Get urgency-appropriate component"""
        return self.response_templates['urgency_responses'].get(urgency_level, "")
    
    def _get_suggestion_component(self, strategy: Dict, context: Dict) -> str:
        """Get context-aware suggestions"""
        suggestions = strategy.get('suggestions', [])
        if not suggestions:
            return ""
        
        # Convert suggestion keys to natural language
        suggestion_texts = []
        for suggestion in suggestions:
            if suggestion == "emergency_services":
                suggestion_texts.append("I'm also including 24/7 emergency service providers.")
            elif suggestion == "related_services":
                suggestion_texts.append("I can also help with related services if needed.")
            elif suggestion == "basic_explanations":
                suggestion_texts.append("I'll include providers who offer clear explanations for beginners.")
        
        return " ".join(suggestion_texts)
    
    def _select_random(self, items: List) -> str:
        """Select random item from list"""
        import random
        return random.choice(items) if items else ""
    
    async def generate_thinking_feedback(self, thinking_result: Dict) -> str:
        """Generate verbal feedback about the thinking process"""
        analysis = thinking_result['analysis']
        
        if analysis['urgency_level'] >= 4:
            return "I can see this is urgent. Let me act quickly."
        elif analysis['emotional_state'] == "concerned":
            return "I understand this is important. Let me find the right help."
        elif analysis['context_awareness']['is_follow_up']:
            return "Based on our previous conversation, let me refine the search."
        else:
            return "Let me analyze your requirements and find the best options."

print("🎯 AdaptiveResponseGenerator class defined")
