#!/usr/bin/env python3
"""
Butler Voice Assistant - Simple Test
"""
import os
import sys

print("🚀 Testing Butler Voice Assistant...")

# Add the project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

print(f"📁 Python path includes: {project_root}")

try:
    print("1. Testing config import...")
    from config.config import Config
    print("✅ Config imported successfully!")
    
    print("2. Creating config object...")
    config = Config()
    print("✅ Config object created!")
    
    print("3. Testing other imports...")
    from utils.logger import setup_logging
    print("✅ Logger imported!")
    
    setup_logging()
    print("✅ Logger setup complete!")
    
    print("🎉 ALL SYSTEMS GO! Butler is working correctly!")
    print(f"📁 Project: {config.APP_NAME}")
    print(f"📍 Default location: {config.DEFAULT_LOCATION}")
    
    input("Press Enter to start voice features...")
    
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    print("Let me check the files...")
    
    # Check if files exist
    config_path = os.path.join(project_root, "src", "config", "config.py")
    logger_path = os.path.join(project_root, "src", "utils", "logger.py")
    
    print(f"Config file exists: {os.path.exists(config_path)}")
    print(f"Logger file exists: {os.path.exists(logger_path)}")
    
    if os.path.exists(config_path):
        print("📄 Config file content (first 10 lines):")
        with open(config_path, 'r') as f:
            for i, line in enumerate(f):
                if i < 10:
                    print(f"   {line.strip()}")
                else:
                    print("   ...")
                    break
    
    input("Press Enter to exit...")
except Exception as e:
    print(f"❌ ERROR: {e}")
    input("Press Enter to exit...")