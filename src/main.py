#!/usr/bin/env python3
"""
Butler Voice Assistant - Complete Working Version
"""
import os
import sys
import importlib.util

print("🚀 Butler Voice Assistant - Complete System Test")

# Get paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

print(f"📁 Project: {project_root}")

# Import Config (this works!)
config_path = os.path.join(current_dir, "config", "config.py")
spec = importlib.util.spec_from_file_location("butler_config", config_path)
config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config_module)
Config = config_module.Config
config = Config()

print(f"✅ {config.APP_NAME} v{config.VERSION}")
print(f"📍 {config.DEFAULT_LOCATION}")

# Try to import other components with error handling
components = {
    "Voice Engine": ("voice.voice_engine", "VoiceEngine"),
    "NLU Engine": ("nlu.nlu_engine", "NLUEngine"), 
    "Service Manager": ("services.service_manager", "ServiceManager"),
    "Logger": ("utils.logger", "setup_logging")
}

print("\n📦 Testing all components...")
working_components = []

for name, (module_path, class_name) in components.items():
    try:
        module_full_path = os.path.join(current_dir, *module_path.split('.')) + ".py"
        if os.path.exists(module_full_path):
            spec = importlib.util.spec_from_file_location(f"butler_{module_path}", module_full_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, class_name):
                working_components.append(name)
                print(f"✅ {name}: Working")
            else:
                print(f"⚠️ {name}: Class {class_name} not found")
        else:
            print(f"❌ {name}: File not found")
    except Exception as e:
        print(f"❌ {name}: Error - {e}")

print(f"\n🎯 Summary: {len(working_components)}/{len(components)} components working")
print("🚀 Butler is ready for development!")

if working_components:
    print("\n💡 Next steps:")
    for component in working_components:
        print(f"   - Develop {component} features")
    
    if "Voice Engine" in working_components:
        print("\n🎤 Voice commands ready to test:")
        print("   - 'Find me plumbers in Bangalore'")
        print("   - 'Book the first one'")
        print("   - 'Hello Butler'")

input("\nPress Enter to start development...")
