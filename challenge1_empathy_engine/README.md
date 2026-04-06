# The Empathy Engine 🎙

**Emotion-Aware Text-to-Speech System**

Give AI a human voice by dynamically modulating vocal characteristics based on detected emotions in text.

## Overview

The Empathy Engine bridges the gap between text-based sentiment and expressive, human-like audio output. It analyzes text emotion and adjusts voice parameters (rate, pitch, volume) to create emotionally resonant speech that sounds natural and engaging.

## Features

✅ **Emotion Detection**: Classifies text into 7 emotions (joy, sadness, anger, fear, surprise, disgust, neutral)  
✅ **Voice Modulation**: Adjusts rate, pitch, and volume based on detected emotion  
✅ **Intensity Scaling**: Emotion strength affects modulation degree  
✅ **Web Interface**: Interactive UI with instant audio playback  
✅ **CLI Mode**: Command-line interface for batch processing  
✅ **Audio Export**: Generates .wav files for each synthesis

## Supported Emotions & Voice Mappings

| Emotion | Rate | Pitch | Volume | Description |
|---------|------|-------|--------|-------------|
| **Joy** | 1.3x | +40 | 0.95 | Fast, high-pitched, cheerful |
| **Sadness** | 0.75x | -30 | 0.70 | Slow, low-pitched, quiet |
| **Anger** | 1.4x | +20 | 1.00 | Fast, intense, loud |
| **Fear** | 1.2x | +30 | 0.80 | Quick, high-pitched, trembling |
| **Surprise** | 1.5x | +50 | 0.95 | Very fast, very high-pitched |
| **Disgust** | 0.9x | -20 | 0.85 | Slow, low, contemptuous |
| **Neutral** | 1.0x | 0 | 0.90 | Normal pace and tone |

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Navigate to the project directory:**
   ```bash
   cd challenge1_empathy_engine
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data (required for TextBlob):**
   ```bash
   python -m textblob.download_corpora
   ```

## Usage

### Web Interface (Recommended)

1. **Start the web server:**
   ```bash
   python app.py
   ```

2. **Open your browser:**
   - Navigate to `http://localhost:8000`
   - Enter text in the text area
   - Click "Generate Emotional Speech"
   - Listen to the generated audio with emotion-appropriate voice modulation

### Command-Line Interface

1. **Interactive mode:**
   ```bash
   python empathy_engine_cli.py
   ```
   Then enter text when prompted.

2. **Single command:**
   ```bash
   python empathy_engine_cli.py "I am so excited about this amazing news!"
   ```

3. **Output:**
   - Audio files are saved to `../outputs/audio/`
   - Filenames include emotion and timestamp: `empathy_engine_joy_20260406_123456.wav`

## Example Usage

```python
from emotion_detector import EmotionDetector
from tts_engine import TTSEngine
from voice_modulator import VoiceModulator

# Initialize components
detector = EmotionDetector()
tts = TTSEngine()
modulator = VoiceModulator(enable_intensity_scaling=True)

# Analyze text
text = "I'm so happy about this!"
emotion, confidence = detector.get_emotion_intensity(text)

# Get voice parameters
params = modulator.get_voice_parameters(emotion, confidence)

# Generate speech
tts.synthesize_to_file(
    text, 
    "output.wav",
    rate_multiplier=params['rate_multiplier'],
    pitch_offset=params['pitch_offset'],
    volume=params['volume']
)
```

## Design Decisions

### Emotion Detection Strategy
- **Hybrid Approach**: Combines keyword matching with sentiment analysis
- **TextBlob**: Provides polarity (-1 to +1) and subjectivity (0 to 1) scores
- **Keyword Patterns**: Enhanced accuracy for emotional expressions
- **Fallback Logic**: Uses sentiment when no keywords match

### Voice Parameter Mapping
- **Non-Linear Scaling**: Uses square root for intensity factor (more natural sounding)
- **Confidence-Based**: Higher emotion confidence = stronger modulation
- **Range Clamping**: Prevents extreme values that sound unnatural
- **Multiple Parameters**: Combines rate, pitch, and volume for rich expressiveness

### Intensity Scaling Algorithm
```python
intensity_factor = 0.3 + 0.7 * sqrt(confidence)
```
- Minimum 30% effect even at low confidence
- Non-linear growth makes differences more noticeable at higher confidence
- Prevents monotonic delivery while avoiding overmodulation

### TTS Engine Choice
- **pyttsx3**: Offline, fast, cross-platform
- **Native Voices**: Uses system voices for reliability
- **Real-time**: No API calls or internet required
- **Trade-off**: Less natural than cloud TTS, but instant and free

## Project Structure

```
challenge1_empathy_engine/
├── app.py                    # FastAPI web application
├── empathy_engine_cli.py     # Command-line interface
├── emotion_detector.py       # Emotion detection module
├── tts_engine.py            # Text-to-speech engine wrapper
├── voice_modulator.py       # Emotion-to-voice mapping logic
├── requirements.txt         # Python dependencies
├── templates/
│   └── index.html          # Web UI template
└── README.md               # This file
```

## API Endpoints

### `GET /`
Returns the web interface HTML.

### `POST /generate`
Generate emotional speech from text.

**Request Body:**
```
form-data:
  text: string (the text to convert to speech)
```

**Response:**
```json
{
  "success": true,
  "text": "I am so excited!",
  "emotion": "joy",
  "confidence": 0.90,
  "all_emotions": {
    "joy": 0.90,
    "neutral": 0.33,
    ...
  },
  "voice_parameters": {
    "rate_multiplier": 1.29,
    "pitch_offset": 38.7,
    "volume": 0.97,
    "description": "Fast, high-pitched, cheerful"
  },
  "audio_file": "empathy_joy_20260406_123456.wav"
}
```

### `GET /audio/{filename}`
Serves the generated audio file.

### `GET /emotions`
Returns information about all supported emotions and their voice parameters.

## Future Enhancements

- ✨ SSML support for fine-grained control
- 🎭 Multiple voice personalities
- 🌍 Multi-language support
- ☁️ Cloud TTS integration (Google/Azure/Amazon)
- 📊 Emotion intensity visualization
- 🎨 Customizable voice parameter mappings

## Technical Requirements Met

✅ **Text Input**: CLI and Web API  
✅ **Emotion Detection**: 7 distinct emotional categories  
✅ **Vocal Parameter Modulation**: Rate, pitch, and volume  
✅ **Emotion-to-Voice Mapping**: Clear, demonstrable logic with intensity scaling  
✅ **Audio Output**: .wav files  
✅ **Bonus - Web Interface**: FastAPI + HTML with audio player  
✅ **Bonus - Intensity Scaling**: Confidence-based modulation  
✅ **Bonus - Granular Emotions**: 7 emotions beyond simple positive/negative/neutral

## License

MIT License - Feel free to use and modify!

## Author

Created as part of the Darwix AI Intern Assessment Challenge.
