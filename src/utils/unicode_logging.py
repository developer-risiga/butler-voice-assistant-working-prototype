import logging
import sys
import os

class UnicodeSafeFormatter(logging.Formatter):
    """Custom formatter that safely handles Unicode characters"""
    def format(self, record):
        try:
            result = super().format(record)
            # On Windows, replace problematic Unicode characters
            if sys.platform == "win32":
                # Replace common emojis with text equivalents
                emoji_replacements = {
                    '🎯': '>>>',
                    '⚡': '***', 
                    '🔄': '>>>',
                    '✅': '>>>',
                    '❌': '!!!',
                    '⚠️': '***',
                    '🔊': '>>>',
                    '🧠': '>>>',
                    '📊': '>>>',
                    '💾': '>>>',
                    '💭': '>>>',
                    '🤔': '>>>',
                    '🏭': '>>>',
                    '💡': '>>>',
                    '🎤': '>>>',
                    '📋': '>>>',
                    '⏹️': '>>>',
                    '🎪': '>>>',
                    '📈': '>>>',
                    '🔧': '>>>',
                    '🚀': '>>>',
                    '🔚': '>>>',
                    '💥': '>>>',
                    '🛑': '>>>',
                    '👤': '>>>'
                }
                for emoji, replacement in emoji_replacements.items():
                    result = result.replace(emoji, replacement)
            return result
        except UnicodeEncodeError:
            # Fallback: remove problematic characters
            return super().format(record).encode('ascii', 'ignore').decode('ascii')

def setup_unicode_safe_logging():
    """Setup logging that works with Unicode characters on all platforms"""
    root_logger = logging.getLogger()
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create handler
    handler = logging.StreamHandler(sys.stdout)
    
    # Create Unicode-safe formatter
    formatter = UnicodeSafeFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Add handler to root logger
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
    
    return root_logger
