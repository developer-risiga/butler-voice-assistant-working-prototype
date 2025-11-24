import json
import os
from datetime import datetime
from typing import Dict, Any

class FeedbackManager:
    """Collects and analyzes user feedback"""
    
    def __init__(self, config):
        self.config = config
        self.feedback_file = os.path.join(config.DATA_DIR, 'feedback.json')
        self.feedback_data = []
    
    async def initialize(self):
        """Initialize feedback system"""
        # Load existing feedback
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'r') as f:
                self.feedback_data = json.load(f)
        return True
    
    async def record_feedback(self, session_id: str, rating: int, comment: str = "", context: Dict = None):
        """Record user feedback"""
        feedback_entry = {
            'session_id': session_id,
            'rating': rating,
            'comment': comment,
            'context': context or {},
            'timestamp': datetime.now().isoformat()
        }
        
        self.feedback_data.append(feedback_entry)
        await self._save_feedback()
        
        print(f"📊 Feedback recorded: {rating}/5 - {comment}")
    
    async def get_feedback_stats(self) -> Dict[str, Any]:
        """Get feedback statistics"""
        if not self.feedback_data:
            return {'total_feedback': 0, 'average_rating': 0}
        
        total = len(self.feedback_data)
        avg_rating = sum(f['rating'] for f in self.feedback_data) / total
        
        return {
            'total_feedback': total,
            'average_rating': round(avg_rating, 2),
            'rating_distribution': self._get_rating_distribution()
        }
    
    def _get_rating_distribution(self) -> Dict[int, int]:
        """Get distribution of ratings"""
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for feedback in self.feedback_data:
            distribution[feedback['rating']] += 1
        return distribution
    
    async def _save_feedback(self):
        """Save feedback to file"""
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)

print("FeedbackManager class defined")
