"""
The Empathy Engine - Web Application
FastAPI web interface for emotion-aware text-to-speech.
"""
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime
from emotion_detector import EmotionDetector
from voice_modulator import VoiceModulator
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI(title="The Empathy Engine", description="Emotion-Aware Text-to-Speech")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Setup static files (if needed)
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup output directory
OUTPUT_DIR = "../outputs/audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Thread pool for TTS generation
executor = ThreadPoolExecutor(max_workers=2)

# Initialize components (global, loaded once at startup)
emotion_detector = None
voice_modulator = None


@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    global emotion_detector, voice_modulator
    print("Initializing The Empathy Engine...")
    print("Loading emotion detector...")
    emotion_detector = EmotionDetector()
    print("Loading voice modulator...")
    voice_modulator = VoiceModulator(enable_intensity_scaling=True)
    print("✅ Ready!")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse("index.html", {"request": request})


def generate_audio_sync(text, output_path, voice_params):
    """
    Synchronous function to generate audio (runs in thread pool).
    Creates a fresh TTS engine for each request to avoid blocking.
    """
    from tts_engine import TTSEngine
    
    # Create a new TTS engine instance for this request
    tts = TTSEngine()
    
    # Generate the audio
    tts.synthesize_to_file(
        text,
        output_path,
        rate_multiplier=voice_params['rate_multiplier'],
        pitch_offset=voice_params['pitch_offset'],
        volume=voice_params['volume']
    )
    
    return output_path


@app.post("/generate")
async def generate_speech(text: str = Form(...)):
    """
    Generate emotional speech from text.
    
    Args:
        text: Input text to convert to speech
        
    Returns:
        JSON with emotion analysis and audio file path
    """
    # Detect emotion
    emotion_result = emotion_detector.detect_emotion(text)
    emotion = emotion_result['primary_emotion']
    confidence = emotion_result['confidence']
    
    # Get voice parameters
    voice_params = voice_modulator.get_voice_parameters(emotion, confidence)
    
    # Generate audio filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"empathy_{emotion}_{timestamp}.wav"
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    # Generate speech in thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        executor,
        generate_audio_sync,
        text,
        output_path,
        voice_params
    )
    
    return {
        "success": True,
        "text": text,
        "emotion": emotion,
        "confidence": confidence,
        "all_emotions": emotion_result['all_emotions'],
        "voice_parameters": {
            "rate_multiplier": voice_params['rate_multiplier'],
            "pitch_offset": voice_params['pitch_offset'],
            "volume": voice_params['volume'],
            "description": voice_params['description']
        },
        "audio_file": filename
    }


@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """Serve audio files."""
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/wav")
    return {"error": "File not found"}, 404


@app.get("/emotions")
async def get_emotions_info():
    """Get information about all supported emotions."""
    return voice_modulator.get_all_emotions_info()


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🎙  Starting The Empathy Engine Web Server")
    print("="*60 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8005)
