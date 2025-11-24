#!/usr/bin/env python3
"""
Butler - Using New Config File
"""
import os
import sys
import importlib.util

print("🚀 Butler - Testing with new config file")

config_path = os.path.join(os.path.dirname(__file__), "config", "config_new.py")
print(f"📁 Using: {config_path}")

try:
    spec = importlib.util.spec_from_file_location("myconfig", config_path)
    myconfig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(myconfig)
    
    Config = myconfig.Config
    config = Config()
    print(f"🎉 SUCCESS! {config.APP_NAME} is working!")
    
except Exception as e:
    print(f"❌ Failed: {e}")

input("Press Enter...")
