import logging
import random
from typing import Dict, List
import asyncio

class RealServiceScenarios:
    """REAL-TIME service scenario handler with dynamic responses"""
    
    def __init__(self):
        self.logger = logging.getLogger("butler.scenarios")
        self.service_categories = {
            'plumber': {
                'common_issues': ['leaking pipes', 'clogged drains', 'running toilets', 'low water pressure', 'water heater issues'],
                'emergency_keywords': ['flood', 'burst pipe', 'water everywhere', 'major leak'],
                'average_costs': {'small': '₹500-₹1500', 'medium': '₹1500-₹4000', 'large': '₹4000-₹10000'}
            },
            'electrician': {
                'common_issues': ['power outage', 'flickering lights', 'outlet not working', 'switch problems', 'wiring issues'],
                'emergency_keywords': ['sparks', 'smoke', 'burning smell', 'electrical fire'],
                'average_costs': {'small': '₹600-₹2000', 'medium': '₹2000-₹5000', 'large': '₹5000-₹15000'}
            },
            'cleaner': {
                'common_issues': ['regular cleaning', 'deep cleaning', 'move-in cleaning', 'move-out cleaning', 'office cleaning'],
                'emergency_keywords': [],
                'average_costs': {'per_hour': '₹200-₹500', 'per_room': '₹500-₹1500'}
            },
            'carpenter': {
                'common_issues': ['furniture repair', 'custom furniture', 'cabinet installation', 'door repair', 'woodworking'],
                'emergency_keywords': [],
                'average_costs': {'small': '₹800-₹2500', 'medium': '₹2500-₹8000', 'large': '₹8000-₹25000'}
            },
            'ac_repair': {
                'common_issues': ['not cooling', 'strange noises', 'water leakage', 'not turning on', 'gas refill'],
                'emergency_keywords': ['no cooling in heat', 'electrical issues'],
                'average_costs': {'service': '₹500-₹1500', 'repair': '₹1500-₹6000', 'gas_refill': '₹1500-₹4000'}
            }
        }
    
    async def get_emergency_response(self, service_type: str, user_input: str) -> str:
        """Generate real-time emergency responses"""
        
        emergency_templates = {
            'plumber': [
                "🚨 PLUMBING EMERGENCY! I'm contacting emergency plumbers in your area immediately. Please turn off your main water valve if there's a major leak. Help is on the way!",
                "🚨 WATER EMERGENCY DETECTED! I'm dispatching emergency plumbers right now. Can you safely contain the water while I get you help?",
                "🚨 URGENT PLUMBING ASSISTANCE! Emergency plumbers are being notified. What's your exact location for fastest response?"
            ],
            'electrician': [
                "🚨 ELECTRICAL EMERGENCY! I'm contacting emergency electricians immediately. If there are sparks or smoke, please turn off the main power if safe to do so.",
                "🚨 URGENT ELECTRICAL ISSUE! Emergency electricians are being dispatched. Please stay away from the affected area while I get you help.",
                "🚨 ELECTRICAL SAFETY ALERT! I'm connecting you with emergency electricians right now. What's your location for immediate assistance?"
            ],
            'general': [
                "🚨 EMERGENCY SITUATION! I'm finding emergency service providers in your area immediately. What's your exact location for fastest response?",
                "🚨 URGENT ASSISTANCE! Emergency professionals are being contacted. Please share your location for immediate help.",
                "🚨 EMERGENCY MODE ACTIVATED! I'm getting you immediate assistance. What's your current location?"
            ]
        }
        
        return random.choice(emergency_templates.get(service_type, emergency_templates['general']))
    
    async def get_service_details_prompt(self, service_type: str, user_input: str = "") -> str:
        """Get dynamic service-specific questions"""
        
        service_info = self.service_categories.get(service_type, {})
        common_issues = service_info.get('common_issues', [])
        
        detail_prompts = {
            'plumber': [
                f"What specific plumbing issue are you facing? Common problems include {', '.join(common_issues[:3])}.",
                f"Plumbers specialize in different areas. Is it {random.choice(common_issues)} or something else?",
                f"To find the right plumber, could you describe the issue? Examples: {', '.join(common_issues[:2])}."
            ],
            'electrician': [
                f"What electrical problem are you experiencing? Typical issues are {', '.join(common_issues[:3])}.",
                f"Electricians have different specialties. Is it {random.choice(common_issues)} or another issue?",
                f"Could you describe the electrical situation? Common problems include {', '.join(common_issues[:2])}."
            ],
            'cleaner': [
                f"What type of cleaning service do you need? Options include {', '.join(common_issues[:3])}.",
                f"Cleaners specialize in different services. Are you looking for {random.choice(common_issues)}?",
                f"What's the scope of cleaning? I can help with {', '.join(common_issues[:2])} and more."
            ],
            'carpenter': [
                f"What carpentry work do you need? Common projects include {', '.join(common_issues[:3])}.",
                f"Carpenters specialize in different areas. Is it {random.choice(common_issues)} or custom work?",
                f"What's your carpentry project about? I can help with {', '.join(common_issues[:2])}."
            ],
            'ac_repair': [
                f"What's the issue with your AC? Common problems are {', '.join(common_issues[:3])}.",
                f"AC technicians specialize in different repairs. Is it {random.choice(common_issues)}?",
                f"Could you describe the AC problem? Typical issues include {', '.join(common_issues[:2])}."
            ]
        }
        
        return random.choice(detail_prompts.get(service_type, detail_prompts['plumber']))
    
    async def get_timing_question(self, service_type: str) -> str:
        """Get service-appropriate timing questions"""
        
        timing_questions = {
            'plumber': [
                "When would you like the plumbing service? Emergency issues can often be addressed within hours.",
                "What's your preferred timing for the plumbing repair? I can find available slots today or tomorrow.",
                "When should the plumber visit? I'll check real-time availability."
            ],
            'electrician': [
                "When do you need the electrical work done? Safety issues are prioritized for immediate attention.",
                "What's your schedule for the electrical service? I can find technicians available soon.",
                "When would you like the electrician to come? I'll check current availability."
            ],
            'cleaner': [
                "When would you like the cleaning service? I can schedule for today, tomorrow, or your preferred date.",
                "What's your preferred cleaning schedule? Morning, afternoon, or specific timing?",
                "When should the cleaner arrive? I'll find available time slots."
            ],
            'carpenter': [
                "When do you need the carpentry work? Projects can typically be scheduled within 1-3 days.",
                "What's your timeline for the carpentry project? I'll find available carpenters.",
                "When should the carpenter start? I'll check availability for your project."
            ],
            'ac_repair': [
                "When do you need AC repair? Cooling issues are often addressed within 24 hours.",
                "What's your preferred timing for AC service? I can find available technicians.",
                "When should the AC technician visit? I'll check real-time availability."
            ]
        }
        
        return random.choice(timing_questions.get(service_type, timing_questions['plumber']))
    
    async def get_location_question(self) -> str:
        """Get location questions"""
        
        location_questions = [
            "What's your complete address? This helps me find professionals serving your exact location.",
            "Could you share your full address? I need this to locate the nearest available service providers.",
            "What's your street address and area? This ensures I find professionals who serve your location."
        ]
        
        return random.choice(location_questions)
    
    async def get_cost_estimate(self, service_type: str, issue_description: str) -> str:
        """Provide realistic cost estimates"""
        
        service_info = self.service_categories.get(service_type, {})
        costs = service_info.get('average_costs', {})
        
        if service_type == 'plumber':
            estimate = f"Plumbing services typically cost {costs.get('small', '₹500-₹2000')} for minor issues, {costs.get('medium', '₹1500-₹4000')} for moderate repairs."
        elif service_type == 'electrician':
            estimate = f"Electrical work usually ranges from {costs.get('small', '₹600-₹2000')} for small fixes to {costs.get('large', '₹5000-₹15000')} for major wiring."
        elif service_type == 'cleaner':
            estimate = f"Cleaning services cost approximately {costs.get('per_hour', '₹200-₹500')} per hour or {costs.get('per_room', '₹500-₹1500')} per room."
        elif service_type == 'carpenter':
            estimate = f"Carpentry work typically costs {costs.get('small', '₹800-₹2500')} for small repairs to {costs.get('large', '₹8000-₹25000')} for custom projects."
        elif service_type == 'ac_repair':
            estimate = f"AC services range from {costs.get('service', '₹500-₹1500')} for servicing to {costs.get('repair', '₹1500-₹6000')} for repairs."
        else:
            estimate = "Cost depends on the specific service requirements. I'll provide exact pricing once we select a professional."
        
        return estimate
    
    async def get_booking_confirmation(self, service_type: str, details: Dict) -> str:
        """Generate booking confirmation message"""
        
        problem = details.get('problem', 'the issue')
        timing = details.get('timing', 'your preferred time')
        location = details.get('location', 'your location')
        
        confirmations = [
            f"✅ Ready to book your {service_type} service!\n\nIssue: {problem}\nTiming: {timing}\nLocation: {location}\n\nShould I proceed with finding available professionals?",
            f"📋 Booking Summary:\n• Service: {service_type}\n• Problem: {problem}\n• When: {timing}\n• Where: {location}\n\nReady to confirm and find professionals?",
            f"🎯 Here's your service request:\n{service_type.title()} for: {problem}\nScheduled: {timing}\nLocation: {location}\n\nShall I book this now?"
        ]
        
        return random.choice(confirmations)
