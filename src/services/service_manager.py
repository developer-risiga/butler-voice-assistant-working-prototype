import asyncio
import logging
from typing import List, Dict, Any

class ServiceManager:
    """Manager for service discovery and booking"""
    
    def __init__(self):
        self.logger = logging.getLogger("butler.services")
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize service manager"""
        self.logger.info("Service Manager initialized")
        self.is_initialized = True
        return True
    
    async def find_services(self, service_type: str, location: str = None) -> Dict[str, Any]:
        """Find services of specified type in location"""
        self.logger.info(f"Finding {service_type} services in {location}")
        
        # Use the actual service_type instead of hardcoding "plumber"
        vendors = self._get_mock_vendors(service_type, location)
        
        response_text = f"Found {len(vendors)} {service_type} services in {location}"
        
        return {
            'success': True,
            'vendors': vendors,
            'response_text': response_text,
            'service_type': service_type,
            'location': location
        }
    
    def _get_mock_vendors(self, service_type: str, location: str) -> List[Dict]:
        """Get mock vendor data based on service type"""
        service_names = {
            'plumber': 'Plumber',
            'electrician': 'Electrician',
            'carpenter': 'Carpenter',
            'cleaner': 'Cleaner',
            'painter': 'Painter'
        }
        
        service_name = service_names.get(service_type, service_type.title())
        
        vendors = [
            {
                'name': f'ABC {service_name} Services',
                'rating': 4.5,
                'phone': '+91-9876543210',
                'address': f'123 Main Street, {location}',
                'distance': '1.2 km',
                'specialization': f'Residential {service_name}'
            },
            {
                'name': f'QuickFix {service_name}',
                'rating': 4.3,
                'phone': '+91-9876543211', 
                'address': f'456 Market Road, {location}',
                'distance': '2.1 km',
                'specialization': f'Commercial {service_name}'
            },
            {
                'name': f'Pro {service_name} Experts',
                'rating': 4.7,
                'phone': '+91-9876543212',
                'address': f'789 Business Park, {location}',
                'distance': '3.5 km',
                'specialization': f'Emergency {service_name}'
            }
        ]
        
        return vendors
    
    async def book_service(self, vendor_index: int, context: Dict = None) -> Dict[str, Any]:
        """Book a service with the specified vendor"""
        self.logger.info(f"Booking service with vendor index: {vendor_index}")
        
        service_type = context.get('service_type', 'service') if context else 'service'
        
        return {
            'success': True,
            'booking_id': f"BK{vendor_index+1}12345",
            'vendor_name': f"Vendor {vendor_index + 1}",
            'service_type': service_type,
            'response_text': f"Booking confirmed for {service_type}! The vendor will contact you within 30 minutes."
        }
    
    async def shutdown(self):
        """Cleanup resources"""
        self.logger.info("Service manager shut down")

print("Updated ServiceManager class defined")
