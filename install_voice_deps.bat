@echo off
chcp 65001 > nul
echo ========================================
echo    Butler Voice Assistant - Dependencies
echo ========================================
echo.

echo 📦 Installing real-time voice dependencies...
echo.

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call .venv\Scripts\activate.bat
)

echo 1. Installing SpeechRecognition...
pip install speechrecognition

echo 2. Installing Whisper (OpenAI speech recognition)...
pip install openai-whisper

echo 3. Installing PyGame for audio playback...
pip install pygame

echo 4. Installing Google Text-to-Speech...
pip install gtts

echo 5. Installing PyAudio for microphone access...
pip install pyaudio

echo 6. Installing NumPy for audio processing...
pip install numpy

echo.
echo ========================================
echo ✅ All voice dependencies installed!
echo.
echo 🚀 Now run Butler with:
echo    python src\main.py
echo.
echo 🎤 Test voice commands:
echo    - "Hello Butler"
echo    - "Find me plumbers"
echo    - "Book a service"
echo.
echo 🔧 If PyAudio fails on Windows, try:
echo    pip install pipwin
echo    pipwin install pyaudio
echo ========================================
echo.
pause
