#!/usr/bin/env python3
"""
Butler Voice Assistant - Main Entry Point
Beta Version 1.0
"""
import asyncio
import signal
import sys
import logging
import os
from datetime import datetime

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config.config import Config
    from utils.logger import setup_logging
    from voice.voice_engine import VoiceEngine
    from nlu.nlu_engine import NLUEngine
    from services.service_manager import ServiceManager
    from conversation.conversation_manager import ConversationManager
    from hardware.hardware_manager import HardwareManager
    from database.db_manager import DatabaseManager
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("📁 Current directory:", os.getcwd())
    print("📁 Script directory:", os.path.dirname(os.path.abspath(__file__)))
    sys.exit(1)