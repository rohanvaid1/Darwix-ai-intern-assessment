"""
Text-to-Speech Engine with Voice Modulation
Converts text to speech with adjustable vocal parameters.
"""
import pyttsx3
import os
from datetime import datetime

class TTSEngine:
    """Text-to-Speech engine with voice parameter control."""
    
    def __init__(self):
        """Initialize the TTS engine."""
        print("Initializing TTS engine...")
        self.engine = pyttsx3.init()
        
        # Get available voices
        self.voices = self.engine.getProperty('voices')
        
        # Set default voice (prefer female voice for more emotional range)
        for voice in self.voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Store default properties
        self.default_rate = self.engine.getProperty('rate')
        self.default_volume = self.engine.getProperty('volume')
        
        print(f"TTS engine initialized! Default rate: {self.default_rate}")
    
    def set_voice_parameters(self, rate_multiplier=1.0, pitch_offset=0, volume=1.0):
        """
        Set voice parameters for speech synthesis.
        
        Args:
            rate_multiplier (float): Speech rate multiplier (0.5 = slow, 2.0 = fast)
            pitch_offset (int): Pitch adjustment (not directly supported by pyttsx3, used for reference)
            volume (float): Volume level (0.0 to 1.0)
        """
        # Calculate new rate
        new_rate = int(self.default_rate * rate_multiplier)
        
        # Clamp values to reasonable ranges
        new_rate = max(50, min(400, new_rate))
        volume = max(0.0, min(1.0, volume))
        
        # Set properties
        self.engine.setProperty('rate', new_rate)
        self.engine.setProperty('volume', volume)
        
        print(f"Voice parameters set: rate={new_rate}, volume={volume:.2f}")
    
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
        
        # Set voice parameters
        self.set_voice_parameters(rate_multiplier, pitch_offset, volume)
        
        # Save to file
        self.engine.save_to_file(text, output_path)
        self.engine.runAndWait()
        
        print(f"Audio saved to: {output_path}")
        return output_path
    
    def speak(self, text, rate_multiplier=1.0, pitch_offset=0, volume=1.0):
        """
        Speak text immediately with specified parameters.
        
        Args:
            text (str): Text to speak
            rate_multiplier (float): Speech rate multiplier
            pitch_offset (int): Pitch adjustment
            volume (float): Volume level
        """
        # Set voice parameters
        self.set_voice_parameters(rate_multiplier, pitch_offset, volume)
        
        # Speak
        self.engine.say(text)
        self.engine.runAndWait()
    
    def reset_to_defaults(self):
        """Reset voice parameters to defaults."""
        self.engine.setProperty('rate', self.default_rate)
        self.engine.setProperty('volume', self.default_volume)


if __name__ == "__main__":
    # Test the TTS engine
    tts = TTSEngine()
    
    test_params = [
        ("Normal speech", 1.0, 0, 0.9),
        ("Fast speech", 1.5, 0, 0.9),
        ("Slow speech", 0.7, 0, 0.9),
        ("Loud speech", 1.0, 0, 1.0),
        ("Quiet speech", 1.0, 0, 0.5),
    ]
    
    print("\n" + "="*60)
    print("TTS ENGINE TESTS")
    print("="*60 + "\n")
    
    for description, rate, pitch, volume in test_params:
        print(f"Testing: {description} (rate={rate}, volume={volume})")
        output_path = f"test_{description.replace(' ', '_').lower()}.wav"
        tts.synthesize_to_file(
            f"This is a test of {description}.",
            output_path,
            rate_multiplier=rate,
            pitch_offset=pitch,
            volume=volume
        )
        print("-" * 60)
    
    print("\nTest complete! Audio files generated.")
