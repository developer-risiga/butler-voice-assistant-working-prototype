#!/usr/bin/env python3
"""
Butler Voice Assistant - Alternative Import Method
"""
import os
import sys
import importlib.util

print("🚀 Butler - Testing Alternative Import")

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, "config", "config.py")

print(f"📁 Config path: {config_path}")
print(f"📁 File exists: {os.path.exists(config_path)}")

# Method 1: Direct file import (bypasses Python cache)
try:
    print("\n🔄 Method 1: Direct file import...")
    spec = importlib.util.spec_from_file_location("config_module", config_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    
    # Check what's in the module
    print("📋 Module contents:")
    for attr in dir(config_module):
        if not attr.startswith('__'):
            value = getattr(config_module, attr)
            print(f"   {attr}: {type(value)}")
    
    if hasattr(config_module, 'Config'):
        Config = config_module.Config
        config = Config()
        print(f"✅ SUCCESS! App: {config.APP_NAME}")
    else:
        print("❌ Config class not found in module")
        
except Exception as e:
    print(f"❌ Method 1 failed: {e}")

# Method 2: Import from different path
try:
    print("\n🔄 Method 2: Import from parent directory...")
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
    
    from src.config.config import Config
    config = Config()
    print(f"✅ SUCCESS! App: {config.APP_NAME}")
    
except Exception as e:
    print(f"❌ Method 2 failed: {e}")

# Method 3: Execute the file directly
try:
    print("\n🔄 Method 3: Execute file directly...")
    with open(config_path, 'r') as f:
        code = f.read()
    
    # Create a temporary namespace
    namespace = {}
    exec(code, namespace)
    
    if 'Config' in namespace:
        Config = namespace['Config']
        config = Config()
        print(f"✅ SUCCESS! App: {config.APP_NAME}")
    else:
        print("❌ Config not found in executed code")
        
except Exception as e:
    print(f"❌ Method 3 failed: {e}")

input("\nPress Enter to exit...")
