# debug_elevenlabs.py
import elevenlabs
from elevenlabs.client import ElevenLabs
from elevenlabs import play

print("🔧 Debugging ElevenLabs imports...")
print(f"ElevenLabs version: {elevenlabs.__version__}")

# Test 1: Check what 'elevenlabs' module contains
print("\n📋 Contents of elevenlabs module:")
for attr in dir(elevenlabs):
    if not attr.startswith('_') and not attr[0].isupper():
        print(f"  - {attr}")

# Test 2: Check if we can create a client
try:
    client = ElevenLabs(api_key="sk_19ea793678ccd614a1a9a880ef5c3d1496908c0cb742ec83")
    print("✅ ElevenLabs client created successfully")
    
    # Test 3: Check if we can get voices
    voices = client.voices.get_all()
    print(f"✅ Voices retrieved: {len(voices.voices)}")
    
    # Test 4: Check if we can generate audio
    audio = client.text_to_speech.convert(
        voice_id="VR6AewLTigWG4xSOukaG",
        text="Hello, this is a test!",
        model_id="eleven_monolingual_v1"
    )
    print("✅ Audio generated successfully")
    
    # Test 5: Check if we can play audio
    play(audio)
    print("✅ Audio played successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
