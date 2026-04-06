"""
The Empathy Engine - CLI Interface
Command-line interface for emotion-aware text-to-speech.
"""
import os
import sys
from datetime import datetime
from emotion_detector import EmotionDetector
from tts_engine import TTSEngine
from voice_modulator import VoiceModulator

class EmpathyEngine:
    """Main application class for The Empathy Engine."""
    
    def __init__(self, output_dir="../outputs/audio"):
        """
        Initialize The Empathy Engine.
        
        Args:
            output_dir (str): Directory for output audio files
        """
        print("\n" + "="*60)
        print("🎙  THE EMPATHY ENGINE - Emotion-Aware TTS")
        print("="*60 + "\n")
        
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize components
        self.emotion_detector = EmotionDetector()
        self.tts_engine = TTSEngine()
        self.voice_modulator = VoiceModulator(enable_intensity_scaling=True)
        
        print("\n✅ All systems ready!\n")
    
    def process_text(self, text, output_filename=None):
        """
        Process text: detect emotion and generate speech.
        
        Args:
            text (str): Input text to process
            output_filename (str): Optional custom output filename
            
        Returns:
            dict: Processing results including audio file path
        """
        print(f"📝 Input text: {text}\n")
        
        # Step 1: Detect emotion
        print("🔍 Analyzing emotion...")
        emotion_result = self.emotion_detector.detect_emotion(text)
        emotion = emotion_result['primary_emotion']
        confidence = emotion_result['confidence']
        
        print(f"   Detected: {emotion.upper()} (confidence: {confidence:.2%})")
        
        # Show top 3 emotions
        top_emotions = sorted(
            emotion_result['all_emotions'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        print(f"   Top emotions: {', '.join([f'{e}: {s:.2%}' for e, s in top_emotions])}")
        
        # Step 2: Get voice parameters
        print("\n🎚  Calculating voice parameters...")
        voice_params = self.voice_modulator.get_voice_parameters(emotion, confidence)
        
        print(f"   Rate: {voice_params['rate_multiplier']:.2f}x")
        print(f"   Pitch: {voice_params['pitch_offset']:+.0f}")
        print(f"   Volume: {voice_params['volume']:.2f}")
        print(f"   Style: {voice_params['description']}")
        
        # Step 3: Generate speech
        print("\n🔊 Generating speech...")
        
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"empathy_engine_{emotion}_{timestamp}.wav"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        audio_path = self.tts_engine.synthesize_to_file(
            text,
            output_path,
            rate_multiplier=voice_params['rate_multiplier'],
            pitch_offset=voice_params['pitch_offset'],
            volume=voice_params['volume']
        )
        
        print(f"✅ Audio generated successfully!")
        print(f"📁 Saved to: {os.path.abspath(audio_path)}\n")
        
        return {
            'text': text,
            'emotion': emotion,
            'confidence': confidence,
            'all_emotions': emotion_result['all_emotions'],
            'voice_parameters': voice_params,
            'audio_path': audio_path
        }


def main():
    """Main CLI function."""
    # Initialize the engine
    engine = EmpathyEngine()
    
    # Check for command-line arguments
    if len(sys.argv) > 1:
        # Process text from command line
        text = ' '.join(sys.argv[1:])
        engine.process_text(text)
    else:
        # Interactive mode
        print("="*60)
        print("Interactive Mode - Enter text to generate emotional speech")
        print("Type 'quit' or 'exit' to stop")
        print("="*60 + "\n")
        
        while True:
            try:
                text = input("Enter text: ").strip()
                
                if text.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if not text:
                    print("⚠️  Please enter some text.\n")
                    continue
                
                print()
                engine.process_text(text)
                print("="*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
