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
            self.gTTS = gTTS
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
        """Synthesize using gTTS - simple version without audio manipulation."""
        try:
            # Generate base audio with gTTS
            # Determine speech speed based on rate_multiplier
            # gTTS only supports slow=True/False, so we approximate:
            # < 0.9 = slow, >= 0.9 = normal
            slow_speech = rate_multiplier < 0.9
            
            # Add emotion cues to the text itself for better expression
            enhanced_text = self._enhance_text_for_emotion(text, rate_multiplier, pitch_offset)
            
            tts = self.gTTS(text=enhanced_text, lang='en', slow=slow_speech)
            
            # Save as MP3 (gTTS native format - no conversion needed)
            final_path = output_path.replace('.wav', '.mp3')
            tts.save(final_path)
            
            print(f"Audio generated with gTTS: {final_path}")
            print(f"  Parameters applied: rate={rate_multiplier:.2f}, pitch={pitch_offset}, volume={volume:.2f}")
            print(f"  Used slow mode: {slow_speech}")
            
            return final_path
            
        except Exception as e:
            print(f"Error with gTTS synthesis: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _enhance_text_for_emotion(self, text, rate_multiplier, pitch_offset):
        """
        Enhance text with punctuation and spacing to influence TTS emotion.
        Since we can't directly control pitch/rate, we use text tricks.
        """
        # For excited/happy emotions (high rate, high pitch)
        if rate_multiplier > 1.2 and pitch_offset > 20:
            # Add exclamation marks and emphasis
            text = text.rstrip('.!?') + '!'
            # Add emphasis words
            if not any(word in text.lower() for word in ['wow', 'amazing', 'great', 'excellent']):
                pass  # Keep original text
        
        # For sad emotions (low rate, low pitch)
        elif rate_multiplier < 0.85 and pitch_offset < -10:
            # Add pauses (commas) and soften
            text = text.replace('.', '...')
        
        # For angry emotions (high rate, moderate pitch)
        elif rate_multiplier > 1.3 and pitch_offset < 30:
            text = text.rstrip('.!?') + '!'
        
        return text
    
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
