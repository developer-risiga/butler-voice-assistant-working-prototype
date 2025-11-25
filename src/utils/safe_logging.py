import logging
import sys
import os

def configure_logging():
    """Configure safe logging for Windows and other systems"""
    try:
        # Set up basic configuration with safe encoding
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[SafeStreamHandler()]
        )
        
        # Apply Windows-specific fixes
        if sys.platform == "win32":
            _fix_windows_unicode()
            
    except Exception as e:
        print(f"Logging configuration warning: {e}")

class SafeStreamHandler(logging.StreamHandler):
    """Safe stream handler that handles Unicode on Windows"""
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            
            # Apply Unicode fixes for Windows
            if sys.platform == "win32":
                msg = _safe_unicode_string(msg)
                
            stream.write(msg + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

def _safe_unicode_string(text):
    """Convert Unicode string to safe representation for Windows"""
    # Replace common problematic emojis
    emoji_map = {
        '🎯': '[TARGET]',
        '⚡': '[PERF]', 
        '🔄': '[SYNC]',
        '✅': '[OK]',
        '❌': '[ERROR]',
        '⚠️': '[WARN]',
        '🔊': '[VOICE]',
        '🧠': '[AI]',
        '📊': '[DATA]',
        '💾': '[MEMORY]',
        '💭': '[THINK]',
        '🤔': '[THINK]',
        '🏭': '[FACTORY]',
        '💡': '[IDEA]',
        '🎤': '[MIC]',
        '📋': '[CLIPBOARD]',
        '⏹️': '[STOP]',
        '🎪': '[DEMO]',
        '📈': '[STATS]',
        '🔧': '[TOOL]',
        '🚀': '[ROCKET]',
        '🔚': '[END]',
        '💥': '[CRASH]',
        '🛑': '[STOP]',
        '👤': '[USER]'
    }
    
    for emoji, replacement in emoji_map.items():
        text = text.replace(emoji, replacement)
    
    return text

def _fix_windows_unicode():
    """Apply Windows-specific Unicode fixes"""
    try:
        # Set console output to UTF-8
        if sys.version_info >= (3, 7):
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass
    
    try:
        # Try to set console code page to UTF-8
        os.system('chcp 65001 > nul 2>&1')
    except:
        pass
