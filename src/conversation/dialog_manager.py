import asyncio
from typing import Dict, Any, List

class DialogManager:
    """Manages multi-step conversations and user prompts"""
    
    def __init__(self):
        self.active_dialogs = {}
        self.conversation_flows = {
            'booking_flow': [
                'confirm_service',
                'get_datetime', 
                'get_contact_info',
                'confirm_booking'
            ],
            'service_search_flow': [
                'get_service_type',
                'get_location',
                'show_results'
            ]
        }
    
    async def start_dialog(self, session_id: str, flow_type: str, initial_context: Dict = None):
        """Start a new conversation flow"""
        self.active_dialogs[session_id] = {
            'flow_type': flow_type,
            'current_step': 0,
            'context': initial_context or {},
            'completed': False
        }
        return await self.get_next_prompt(session_id)
    
    async def get_next_prompt(self, session_id: str) -> str:
        """Get the next prompt in the conversation flow"""
        if session_id not in self.active_dialogs:
            return None
            
        dialog = self.active_dialogs[session_id]
        flow_steps = self.conversation_flows[dialog['flow_type']]
        current_step = flow_steps[dialog['current_step']]
        
        prompts = {
            'confirm_service': "Which service would you like to book?",
            'get_datetime': "When would you like the service? You can say today, tomorrow, or a specific date.",
            'get_contact_info': "Please provide your phone number for confirmation.",
            'confirm_booking': "Shall I confirm this booking?",
            'get_service_type': "What type of service are you looking for?",
            'get_location': "In which area do you need the service?",
            'show_results': "Here are the available service providers:"
        }
        
        return prompts.get(current_step, "How can I help you?")
    
    async process_user_response(self, session_id: str, user_input: str) -> Dict[str, Any]:
        """Process user response and move to next step"""
        if session_id not in self.active_dialogs:
            return {'error': 'No active dialog'}
            
        dialog = self.active_dialogs[session_id]
        current_step = self.conversation_flows[dialog['flow_type']][dialog['current_step']]
        
        # Process based on current step
        if current_step == 'get_service_type':
            dialog['context']['service_type'] = user_input
        elif current_step == 'get_location':
            dialog['context']['location'] = user_input
        elif current_step == 'get_datetime':
            dialog['context']['datetime'] = user_input
        elif current_step == 'get_contact_info':
            dialog['context']['phone'] = user_input
        
        # Move to next step
        dialog['current_step'] += 1
        flow_steps = self.conversation_flows[dialog['flow_type']]
        
        if dialog['current_step'] >= len(flow_steps):
            dialog['completed'] = True
            return {
                'completed': True,
                'context': dialog['context'],
                'next_prompt': None
            }
        else:
            next_prompt = await self.get_next_prompt(session_id)
            return {
                'completed': False,
                'context': dialog['context'],
                'next_prompt': next_prompt
            }
    
    async def get_dialog_context(self, session_id: str) -> Dict:
        """Get current dialog context"""
        return self.active_dialogs.get(session_id, {})

print("DialogManager class defined")
