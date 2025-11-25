import logging
import random
from typing import Dict

class RealServiceScenarios:
    """Handle real-world service scenarios with detailed responses"""
    
    def __init__(self):
        self.logger = logging.getLogger("butler.scenarios")
        
    async def get_emergency_response(self, service_type: str) -> str:
        """Generate emergency response for different services"""
        
        emergency_responses = {
            "plumber": [
                "I understand this is a plumbing emergency! Let me find emergency plumbers in your area immediately. First, can you tell me if there's active water leaking and your location?",
                "Plumbing emergency noted! I'll connect you with emergency plumbers right away. Please tell me your location and the severity of the leak.",
                "Emergency plumbing help is on the way! I need your location to find the nearest available plumbers."
            ],
            "electrician": [
                "Electrical emergency! Safety first - I'm finding emergency electricians. Are there any sparks, smoke, or immediate dangers? Please share your location.",
                "Emergency electrical situation! I'll get you certified electricians immediately. What's the specific emergency and your location?",
                "Electrical emergency assistance! I'm connecting you with emergency electricians. Please describe the situation and share your location."
            ],
            "general": [
                "Emergency situation! I'm finding service providers immediately. What's the emergency and your location?",
                "Emergency assistance activated! I need your location to find the nearest available help.",
                "Emergency services are being contacted! Please share your location and describe the urgent situation."
            ]
        }
        
        return random.choice(emergency_responses.get(service_type, emergency_responses["general"]))
    
    async def get_service_details_prompt(self, service_type: str) -> str:
        """Get appropriate follow-up questions for each service type"""
        
        detail_prompts = {
            "plumber": [
                "To find the right plumber, could you tell me: Is it a leak, clogged drain, toilet issue, or something else?",
                "What specific plumbing problem are you facing? This helps me match you with the right specialist.",
                "Plumbers specialize in different areas. What exactly needs repair or installation?"
            ],
            "electrician": [
                "Electricians have different specialties. Are you dealing with wiring, outlets, lighting, or appliance issues?",
                "What specific electrical work do you need? This helps me find the right certified electrician.",
                "Could you describe the electrical issue? Is it repairs, installations, or emergency fixes?"
            ],
            "cleaner": [
                "What type of cleaning service do you need? Regular cleaning, deep cleaning, or move-in/move-out cleaning?",
                "How many rooms need cleaning and what's your preferred schedule?",
                "What areas need attention? Entire home, specific rooms, or special requirements?"
            ],
            "carpenter": [
                "What carpentry work do you need? Furniture repair, custom work, or installations?",
                "Carpenters specialize in different areas. What specific project are you working on?",
                "What type of woodwork do you need? Repairs, new furniture, or modifications?"
            ],
            "ac_repair": [
                "What's the issue with your AC? Not cooling, strange noises, or not turning on?",
                "AC problems vary. Is it cooling issues, water leakage, or electrical problems?",
                "What specific AC problem are you experiencing? This helps me find the right technician."
            ]
        }
        
        return random.choice(detail_prompts.get(service_type, detail_prompts["plumber"]))
    
    async def get_timing_question(self) -> str:
        """Ask about service timing"""
        
        timing_questions = [
            "When would you like this service to be completed? Are you flexible on timing?",
            "What's your preferred schedule for this service? Today, tomorrow, or specific date?",
            "When do you need the service done? I can check availability for your preferred timing."
        ]
        
        return random.choice(timing_questions)
    
    async def get_location_question(self) -> str:
        """Ask about location"""
        
        location_questions = [
            "What's your location? This helps me find service providers in your area.",
            "Could you share your area or location? I'll find professionals nearby.",
            "What's your city or area? I need this to locate service providers close to you."
        ]
        
        return random.choice(location_questions)
