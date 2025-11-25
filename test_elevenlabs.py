# test_elevenlabs.py
import elevenlabs

print("🔧 Testing ElevenLabs installation...")
print(f"ElevenLabs version: {elevenlabs.__version__}")

# Check available attributes
print("Available attributes in elevenlabs module:")
for attr in dir(elevenlabs):
    if not attr.startswith('_'):  # Skip private attributes
        print(f"  - {attr}")

# Test if we can create a client
try:
    from elevenlabs.client import ElevenLabs
    print("✅ ElevenLabs client import successful")
except ImportError as e:
    print(f"❌ ElevenLabs client import failed: {e}")

# Test if we can import play
try:
    from elevenlabs import play
    print("✅ ElevenLabs play import successful")
except ImportError as e:
    print(f"❌ ElevenLabs play import failed: {e}")
