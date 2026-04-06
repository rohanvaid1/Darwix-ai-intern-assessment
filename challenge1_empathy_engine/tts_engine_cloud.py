"""
Cloud-Compatible Text-to-Speech Engine with Voice Modulation
Uses gTTS (Google TTS) which works on all platforms including Linux servers.
Falls back to pyttsx3 on Windows for local development.
"""
import os
import sys
from datetime import datetime

class TTSEngine:
    """Cross-platform Text-to-Speech engine with voice parameter control."""
    
    def __init__(self):
        """Initialize the TTS engine with platform detection."""
        print("Initializing cross-platform TTS engine...")
        
        # Detect platform and choose appropriate TTS
        self.use_gtts = True  # Default to gTTS for cloud compatibility
        
        try:
            # Try importing gTTS first (works on Linux/cloud)
            from gtts import gTTS
            from pydub import AudioSegment
            self.gTTS = gTTS
            self.AudioSegment = AudioSegment
            print("Using gTTS (Google Text-to-Speech) - Cloud compatible!")
        except ImportError:
            # Fall back to pyttsx3 for Windows local dev
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.use_gtts = False
                self.default_rate = self.engine.getProperty('rate')
                self.default_volume = self.engine.getProperty('volume')
                print("Using pyttsx3 - Local development mode")
            except Exception as e:
                print(f"Error initializing TTS: {e}")
                raise
    
    def synthesize_to_file(self, text, output_path, rate_multiplier=1.0, pitch_offset=0, volume=1.0):
        """
        Synthesize text to an audio file with specified parameters.
        
        Args:
            text (str): Text to synthesize
            output_path (str): Path for output audio file
            rate_multiplier (float): Speech rate multiplier
            pitch_offset (int): Pitch adjustment
            volume (float): Volume level
            
        Returns:
            str: Path to the generated audio file
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if self.use_gtts:
            return self._synthesize_with_gtts(text, output_path, rate_multiplier, pitch_offset, volume)
        else:
            return self._synthesize_with_pyttsx3(text, output_path, rate_multiplier, pitch_offset, volume)
    
    def _synthesize_with_gtts(self, text, output_path, rate_multiplier, pitch_offset, volume):
        """Synthesize using gTTS with audio manipulation for emotion."""
        try:
            # Generate base audio with gTTS
            # Determine speech speed (slow for rate < 1.0, normal otherwise)
            slow_speech = rate_multiplier < 0.9
            
            tts = self.gTTS(text=text, lang='en', slow=slow_speech)
            
            # Save to temporary file first
            temp_path = output_path.replace('.wav', '_temp.mp3').replace('.mp3', '_temp.mp3')
            tts.save(temp_path)
            
            # Load and manipulate audio with pydub
            audio = self.AudioSegment.from_mp3(temp_path)
            
            # Apply rate modulation
            if rate_multiplier != 1.0:
                # Speed up or slow down
                speed_factor = rate_multiplier / (0.5 if slow_speech else 1.0)
                if speed_factor != 1.0:
                    # Change frame rate to change speed
                    new_frame_rate = int(audio.frame_rate * speed_factor)
                    audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_frame_rate})
                    audio = audio.set_frame_rate(44100)  # Normalize back
            
            # Apply pitch modulation (octaves conversion)
            if pitch_offset != 0:
                # Convert pitch offset to octaves (-50 to +50 -> -0.5 to +0.5 octaves)
                octaves = pitch_offset / 100.0
                new_sample_rate = int(audio.frame_rate * (2 ** octaves))
                audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
                audio = audio.set_frame_rate(44100)  # Normalize back
            
            # Apply volume modulation
            if volume != 1.0:
                # Convert volume (0.0-1.0) to dB (-40 to +6)
                volume_db = (volume - 0.7) * 20  # Map 0.5-1.0 to roughly -4 to +6 dB
                audio = audio + volume_db
            
            # Export as WAV
            final_path = output_path if output_path.endswith('.wav') else output_path.replace('.mp3', '.wav')
            audio.export(final_path, format='wav')
            
            # Clean up temp file
            try:
                os.remove(temp_path)
            except:
                pass
            
            print(f"Audio generated with gTTS: {final_path}")
            return final_path
            
        except Exception as e:
            print(f"Error with gTTS synthesis: {e}")
            # Fallback: save simple gTTS without manipulation
            tts = self.gTTS(text=text, lang='en')
            simple_path = output_path.replace('.wav', '.mp3')
            tts.save(simple_path)
            print(f"Fallback: Simple audio saved to {simple_path}")
            return simple_path
    
    def _synthesize_with_pyttsx3(self, text, output_path, rate_multiplier, pitch_offset, volume):
        """Synthesize using pyttsx3 (Windows local development)."""
        # Calculate new rate
        new_rate = int(self.default_rate * rate_multiplier)
        new_rate = max(50, min(400, new_rate))
        volume = max(0.0, min(1.0, volume))
        
        # Set properties
        self.engine.setProperty('rate', new_rate)
        self.engine.setProperty('volume', volume)
        
        # Save to file
        self.engine.save_to_file(text, output_path)
        self.engine.runAndWait()
        
        print(f"Audio generated with pyttsx3: {output_path}")
        return output_path


if __name__ == "__main__":
    # Test the TTS engine
    tts = TTSEngine()
    
    test_text = "This is a test of the emotional text to speech engine."
    output_path = "test_outputs/test_audio.wav"
    
    os.makedirs("test_outputs", exist_ok=True)
    
    print("\n" + "="*60)
    print("CROSS-PLATFORM TTS ENGINE TEST")
    print("="*60 + "\n")
    
    result = tts.synthesize_to_file(
        test_text,
        output_path,
        rate_multiplier=1.2,
        pitch_offset=20,
        volume=0.9
    )
    
    print(f"\nTest complete! Audio saved to: {result}")
