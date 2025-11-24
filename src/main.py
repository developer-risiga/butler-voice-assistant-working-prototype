#!/usr/bin/env python3
"""
Butler Voice Assistant - Fixed Import Version
"""
import os
import sys

print("🚀 Butler Voice Assistant - Testing Imports")

# Fix Python path - Add the src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = current_dir  # src folder
project_root = os.path.dirname(current_dir)  # project root folder

print(f"📁 Current directory: {current_dir}")
print(f"📁 Project root: {project_root}")

# Add both paths to Python path
sys.path.insert(0, src_dir)
sys.path.insert(0, project_root)

print(f"🔧 Python path includes: {sys.path}")

try:
    print("1. Testing config import...")
    
    # Try different import methods
    try:
        from config.config import Config
        print("✅ SUCCESS: Imported using 'from config.config import Config'")
    except ImportError:
        try:
            from src.config.config import Config
            print("✅ SUCCESS: Imported using 'from src.config.config import Config'")
        except ImportError:
            # Direct import
            import importlib.util
            spec = importlib.util.spec_from_file_location("config", os.path.join(current_dir, "config", "config.py"))
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            Config = config_module.Config
            print("✅ SUCCESS: Imported using direct file load")
    
    print("2. Creating config object...")
    config = Config()
    print("✅ SUCCESS: Config object created!")
    
    print("3. Testing other imports...")
    from utils.logger import setup_logging
    print("✅ SUCCESS: Logger imported!")
    
    print("🎉 ALL IMPORTS WORKING! BUTLER IS READY! 🎉")
    print(f"📱 App: {config.APP_NAME}")
    print(f"🔢 Version: {config.VERSION}")
    print(f"📍 Location: {config.DEFAULT_LOCATION}")
    
    input("Press Enter to start development...")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("Let me debug the issue...")
    
    # Check if files exist
    config_path = os.path.join(current_dir, "config", "config.py")
    logger_path = os.path.join(current_dir, "utils", "logger.py")
    
    print(f"📄 Config file exists: {os.path.exists(config_path)}")
    print(f"📄 Logger file exists: {os.path.exists(logger_path)}")
    
    # List all Python files in src
    print("📁 Files in src directory:")
    for root, dirs, files in os.walk(current_dir):
        level = root.replace(current_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith('.py'):
                print(f'{subindent}{file}')
    
    input("Press Enter to exit...")