"""
Application constants
"""

# Intent names
INTENT_FIND_SERVICE = "find_service"
INTENT_BOOK_SERVICE = "book_service"
INTENT_GREET = "greet"
INTENT_CANCEL = "cancel"
INTENT_HELP = "help"
INTENT_THANKS = "thanks"

# Service types
SERVICE_PLUMBER = "plumber"
SERVICE_ELECTRICIAN = "electrician"
SERVICE_CARPENTER = "carpenter"
SERVICE_CLEANER = "cleaner"
SERVICE_PEST_CONTROL = "pest_control"

SERVICE_TYPES = {
    SERVICE_PLUMBER: "Plumber",
    SERVICE_ELECTRICIAN: "Electrician", 
    SERVICE_CARPENTER: "Carpenter",
    SERVICE_CLEANER: "Cleaner",
    SERVICE_PEST_CONTROL: "Pest Control"
}

# Response templates
RESPONSE_TEMPLATES = {
    "welcome": "Hello! I'm Butler. I can help you find and book local services.",
    "no_services": "I couldn't find any {service_type} services in your area.",
    "services_found": "I found {count} {service_type} services near you:",
    "booking_confirmed": "Booking confirmed with {vendor_name}! They will contact you shortly.",
    "error_general": "I encountered an error. Please try again.",
    "not_understood": "I'm not sure I understand. You can ask me to find plumbers, electricians, or other services."
}

# Audio settings
AUDIO_FORMATS = {
    'sample_rate': 16000,
    'channels': 1,
    'sample_width': 2  # 16-bit
}
