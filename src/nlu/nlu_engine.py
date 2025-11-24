import asyncio
import logging
from typing import Dict, Any

class NLUEngine:
    """Improved Natural Language Understanding engine"""
    
    def __init__(self):
        self.logger = logging.getLogger("butler.nlu")
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize NLU engine"""
        self.logger.info("NLU Engine initialized")
        self.is_initialized = True
        return True
    
    async def parse(self, text: str, context: Dict = None) -> Dict[str, Any]:
        """Parse user text and extract intent/entities"""
        text_lower = text.lower()
        
        # Detect service type
        service_type = self._extract_service_type(text_lower)
        
        # Detect intent
        intent = self._detect_intent(text_lower)
        
        # Detect location
        location = self._extract_location(text_lower)
        
        entities = {
            'service_type': service_type,
            'location': location
        }
        
        self.logger.info(f"NLU Result - Intent: {intent}, Service: {service_type}, Location: {location}")
        
        return {
            'intent': intent,
            'confidence': 0.9,
            'entities': entities,
            'text': text
        }
    
    def _detect_intent(self, text: str) -> str:
        """Detect user intent"""
        if any(word in text for word in ['find', 'search', 'need', 'want', 'look for', 'get']):
            return "find_service"
        elif any(word in text for word in ['book', 'schedule', 'appointment', 'reserve']):
            return "book_service"
        elif any(word in text for word in ['hello', 'hi', 'hey', 'greetings']):
            return "greet"
        elif any(word in text for word in ['thank', 'thanks']):
            return "thanks"
        elif any(word in text for word in ['cancel', 'stop']):
            return "cancel"
        else:
            return "unknown"
    
    def _extract_service_type(self, text: str) -> str:
        """Extract service type from text"""
        service_keywords = {
            'plumber': ['plumb', 'pipe', 'water', 'leak', 'drain'],
            'electrician': ['electric', 'wiring', 'power', 'light', 'switch', 'socket'],
            'carpenter': ['carpent', 'wood', 'furniture', 'cabinet', 'table'],
            'cleaner': ['clean', 'housekeeping', 'maid', 'sweep'],
            'painter': ['paint', 'wall', 'color', 'repaint']
        }
        
        for service, keywords in service_keywords.items():
            if any(keyword in text for keyword in keywords):
                return service
        
        # Default to plumber if no specific service detected
        return "plumber"
    
    def _extract_location(self, text: str) -> str:
        """Extract location from text"""
        location_keywords = {
            'bangalore': ['bangalore', 'bengaluru', 'blr'],
            'mumbai': ['mumbai', 'bombay'],
            'delhi': ['delhi', 'new delhi'],
            'chennai': ['chennai', 'madras'],
            'hyderabad': ['hyderabad', 'hyd']
        }
        
        for location, keywords in location_keywords.items():
            if any(keyword in text for keyword in keywords):
                return location
        
        # Default location
        return "Bangalore"
    
    async def shutdown(self):
        """Cleanup resources"""
        self.logger.info("NLU engine shut down")

print("Improved NLUEngine class defined")
