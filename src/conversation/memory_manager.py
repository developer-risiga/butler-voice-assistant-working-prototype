import json
import time
import os
from typing import Dict, List, Any

class MemoryManager:
    """Manages conversation memory and context"""
    
    def __init__(self, config):
        self.config = config
        self.current_session = None
        self.conversation_history = []
        self.user_preferences = {}
        
    async def initialize(self):
        """Initialize memory manager"""
        self.current_session = self._create_new_session()
        return True
    
    def _create_new_session(self) -> Dict[str, Any]:
        """Create a new conversation session"""
        return {
            'session_id': f"session_{int(time.time())}",
            'start_time': time.time(),
            'last_interaction': time.time(),
            'current_service': None,
            'current_vendors': [],
            'pending_booking': None
        }
    
    async def update_conversation(self, user_input: str, system_response: str, intent: str, entities: Dict):
        """Update conversation history and context"""
        # Add to history
        self.conversation_history.append({
            'timestamp': time.time(),
            'user': user_input,
            'system': system_response,
            'intent': intent,
            'entities': entities
        })
        
        # Keep only last 10 interactions
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        # Update context based on intent
        if intent == "find_service":
            self.current_session['current_service'] = entities.get('service_type')
            self.current_session['current_location'] = entities.get('location')
        elif intent == "book_service":
            self.current_session['pending_booking'] = {
                'service_type': entities.get('service_type'),
                'timestamp': time.time()
            }
        
        self.current_session['last_interaction'] = time.time()
    
    async def get_context(self) -> Dict[str, Any]:
        """Get current conversation context"""
        return {
            'session': self.current_session,
            'recent_history': self.conversation_history[-3:] if self.conversation_history else [],
            'user_preferences': self.user_preferences
        }
    
    async def should_restart_session(self) -> bool:
        """Check if session should be restarted (timeout)"""
        if not self.current_session:
            return True
        
        # Restart if no interaction for 10 minutes
        return (time.time() - self.current_session['last_interaction']) > 600
    
    async def restart_session(self):
        """Restart the conversation session"""
        self.current_session = self._create_new_session()
        print("🔄 Conversation session restarted")

print("MemoryManager class defined")
