#!/usr/bin/env python3
"""
Butler Voice Assistant - Working Version
"""
import os
import sys
import importlib.util

print("🚀 Butler Voice Assistant - Starting...")

# Get absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
config_path = os.path.join(current_dir, "config", "config.py")

print(f"📁 Current dir: {current_dir}")
print(f"📁 Project root: {project_root}")
print(f"📁 Config path: {config_path}")

# Clear Python cache
cache_dirs = [
    os.path.join(current_dir, "__pycache__"),
    os.path.join(current_dir, "config", "__pycache__")
]
for cache_dir in cache_dirs:
    if os.path.exists(cache_dir):
        import shutil
        shutil.rmtree(cache_dir)
        print(f"🧹 Cleared cache: {cache_dir}")

# Method 1: Direct file import (BYPASSES ALL IMPORT ISSUES)
print("\n🔄 Method 1: Direct file import...")
try:
    spec = importlib.util.spec_from_file_location("butler_config", config_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    
    # Get the Config class
    Config = config_module.Config
    
    # Test it
    config = Config()
    print(f"✅ SUCCESS! App: {config.APP_NAME}")
    print(f"✅ Version: {config.VERSION}")
    print(f"✅ Location: {config.DEFAULT_LOCATION}")
    
except Exception as e:
    print(f"❌ Method 1 failed: {e}")
    sys.exit(1)

# Now import other components
print("\n📦 Loading other components...")
try:
    from utils.logger import setup_logging
    from voice.voice_engine import VoiceEngine
    from nlu.nlu_engine import NLUEngine
    from services.service_manager import ServiceManager
    
    print("✅ All components imported successfully!")
    
except ImportError as e:
    print(f"⚠️ Some components missing: {e}")
    print("But Butler core is working!")

print("\n🎉 BUTLER VOICE ASSISTANT IS READY! 🎉")
print("You can now add the voice features and AI components.")

# Keep the program running
try:
    input("\nPress Enter to exit...")
except:
    pass
