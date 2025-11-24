@echo off
echo 🏭 Butler Production Deployment
echo =================================

echo 1. Installing production dependencies...
pip install aiohttp python-dotenv

echo 2. Creating necessary directories...
mkdir data logs cache 2>nul

echo 3. Setting up production configuration...
if not exist ".env" (
    copy .env.example .env
    echo ⚠️  Please edit .env with your API keys
)

echo 4. Testing production setup...
python -c "import sys; sys.path.append('src'); from voice.voice_engine import VoiceEngine; print('✅ Production imports working')"

echo.
echo =================================
echo 🎉 Production setup complete!
echo 📁 Next: Add your API keys to .env
echo 🚀 Run: python src\main.py
echo =================================
pause
