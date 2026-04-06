"""
The Empathy Engine - Web Application
FastAPI web interface for emotion-aware text-to-speech.
Cloud-compatible version using gTTS.
"""
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import traceback
from datetime import datetime
from emotion_detector import EmotionDetector
from voice_modulator import VoiceModulator
try:
    from tts_engine_cloud import TTSEngine  # Cloud-compatible
except ImportError:
    from tts_engine import TTSEngine  # Fallback to pyttsx3
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
    try:
        # Import cloud-compatible TTS
        try:
            from tts_engine_cloud import TTSEngine
        except ImportError:
            from tts_engine import TTSEngine
        
        # Create a new TTS engine instance for this request
        tts = TTSEngine()
        
        # Generate the audio
        result = tts.synthesize_to_file(
            text,
            output_path,
            rate_multiplier=voice_params['rate_multiplier'],
            pitch_offset=voice_params['pitch_offset'],
            volume=voice_params['volume']
        )
        
        return result
    except Exception as e:
        print(f"Error in generate_audio_sync: {e}")
        traceback.print_exc()
        raise


@app.post("/generate")
async def generate_speech(text: str = Form(...)):
    """
    Generate emotional speech from text.
    
    Args:
        text: Input text to convert to speech
        
    Returns:
        JSON with emotion analysis and audio file path
    """
    try:
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
        result_path = await loop.run_in_executor(
            executor,
            generate_audio_sync,
            text,
            output_path,
            voice_params
        )
        
        # Get actual filename (might be .mp3 instead of .wav)
        actual_filename = os.path.basename(result_path)
        
        return JSONResponse({
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
            "audio_file": actual_filename
        })
    
    except Exception as e:
        print(f"Error in generate_speech: {e}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "details": traceback.format_exc()
            }
        )


@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """Serve audio files (supports both .wav and .mp3)."""
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        # Detect file type
        media_type = "audio/mpeg" if filename.endswith('.mp3') else "audio/wav"
        return FileResponse(file_path, media_type=media_type)
    return JSONResponse({"error": "File not found"}, status_code=404)


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
