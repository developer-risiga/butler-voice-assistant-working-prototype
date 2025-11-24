import random
from typing import List, Dict, Any

class RecommendationEngine:
    """Provides smart vendor recommendations based on user preferences"""
    
    def __init__(self):
        self.user_preferences = {}
    
    async def initialize(self):
        return True
    
    async def get_recommendations(self, service_type: str, user_context: Dict = None) -> List[Dict[str, Any]]:
        """Get smart recommendations based on user preferences and context"""
        all_vendors = await self._get_sample_vendors(service_type)
        
        # Apply recommendation logic
        recommendations = self._apply_recommendation_filters(all_vendors, user_context)
        
        return recommendations[:3]  # Return top 3 recommendations
    
    def _apply_recommendation_filters(self, vendors: List[Dict], user_context: Dict) -> List[Dict]:
        """Apply smart filters to rank vendors"""
        ranked_vendors = []
        
        for vendor in vendors:
            score = 0
            
            # Rating-based scoring (40% weight)
            score += vendor['rating'] * 8
            
            # Experience-based scoring (25% weight)
            experience_years = int(vendor['experience'].split()[0])
            score += min(experience_years, 10) * 2.5
            
            # Review count scoring (20% weight)
            score += min(vendor['reviews'] / 10, 10) * 2
            
            # Response time scoring (15% weight)
            if '15 minutes' in vendor['response_time']:
                score += 15
            elif '30 minutes' in vendor['response_time']:
                score += 10
            else:
                score += 5
            
            vendor['recommendation_score'] = score
            ranked_vendors.append(vendor)
        
        # Sort by recommendation score
        ranked_vendors.sort(key=lambda x: x['recommendation_score'], reverse=True)
        return ranked_vendors
    
    async def _get_sample_vendors(self, service_type: str) -> List[Dict]:
        """Get sample vendor data for recommendations"""
        # This would be replaced with real data
        return [
            {
                'id': 1,
                'name': f'Premium {service_type.title()} Services',
                'rating': 4.8,
                'experience': '6 years',
                'reviews': 120,
                'response_time': '15 minutes',
                'price_range': '₹800 - ₹2500'
            },
            {
                'id': 2, 
                'name': f'Quick {service_type.title()} Solutions',
                'rating': 4.3,
                'experience': '3 years',
                'reviews': 45,
                'response_time': '30 minutes', 
                'price_range': '₹500 - ₹1800'
            },
            {
                'id': 3,
                'name': f'Expert {service_type.title()} Professionals',
                'rating': 4.6,
                'experience': '8 years',
                'reviews': 89,
                'response_time': '20 minutes',
                'price_range': '₹700 - ₹2200'
            }
        ]
    
    async def learn_preference(self, user_id: str, preferred_vendor_id: int, service_type: str):
        """Learn from user preferences to improve recommendations"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        
        if service_type not in self.user_preferences[user_id]:
            self.user_preferences[user_id][service_type] = []
        
        self.user_preferences[user_id][service_type].append(preferred_vendor_id)

print("RecommendationEngine class defined")
