"""
Voice Modulator - Maps emotions to voice parameters
Implements the emotion-to-voice mapping logic with intensity scaling.
"""
import math

class VoiceModulator:
    """Maps detected emotions to voice parameters for TTS."""
    
    # Base emotion-to-voice parameter mappings
    EMOTION_MAPPINGS = {
        'joy': {
            'rate_multiplier': 1.3,
            'pitch_offset': 40,
            'volume': 0.95,
            'description': 'Fast, high-pitched, cheerful'
        },
        'sadness': {
            'rate_multiplier': 0.75,
            'pitch_offset': -30,
            'volume': 0.7,
            'description': 'Slow, low-pitched, quiet'
        },
        'anger': {
            'rate_multiplier': 1.4,
            'pitch_offset': 20,
            'volume': 1.0,
            'description': 'Fast, intense, loud'
        },
        'fear': {
            'rate_multiplier': 1.2,
            'pitch_offset': 30,
            'volume': 0.8,
            'description': 'Quick, high-pitched, trembling'
        },
        'surprise': {
            'rate_multiplier': 1.5,
            'pitch_offset': 50,
            'volume': 0.95,
            'description': 'Very fast, very high-pitched'
        },
        'disgust': {
            'rate_multiplier': 0.9,
            'pitch_offset': -20,
            'volume': 0.85,
            'description': 'Slow, low, contemptuous'
        },
        'neutral': {
            'rate_multiplier': 1.0,
            'pitch_offset': 0,
            'volume': 0.9,
            'description': 'Normal pace and tone'
        }
    }
    
    def __init__(self, enable_intensity_scaling=True):
        """
        Initialize the voice modulator.
        
        Args:
            enable_intensity_scaling (bool): Whether to scale parameters based on emotion intensity
        """
        self.enable_intensity_scaling = enable_intensity_scaling
    
    def get_voice_parameters(self, emotion, confidence=1.0):
        """
        Get voice parameters for a given emotion and confidence level.
        
        Args:
            emotion (str): Detected emotion name
            confidence (float): Confidence score (0.0 to 1.0)
            
        Returns:
            dict: Voice parameters {rate_multiplier, pitch_offset, volume}
        """
        # Get base parameters for the emotion
        if emotion not in self.EMOTION_MAPPINGS:
            emotion = 'neutral'
        
        base_params = self.EMOTION_MAPPINGS[emotion].copy()
        
        if not self.enable_intensity_scaling:
            return {
                'rate_multiplier': base_params['rate_multiplier'],
                'pitch_offset': base_params['pitch_offset'],
                'volume': base_params['volume']
            }
        
        # Apply intensity scaling
        # Use non-linear scaling for more natural results
        intensity_factor = self._calculate_intensity_factor(confidence)
        
        # Scale parameters
        rate_multiplier = self._scale_rate(base_params['rate_multiplier'], intensity_factor)
        pitch_offset = self._scale_pitch(base_params['pitch_offset'], intensity_factor)
        volume = self._scale_volume(base_params['volume'], intensity_factor)
        
        return {
            'rate_multiplier': rate_multiplier,
            'pitch_offset': pitch_offset,
            'volume': volume,
            'emotion': emotion,
            'confidence': confidence,
            'description': base_params['description']
        }
    
    def _calculate_intensity_factor(self, confidence):
        """
        Calculate intensity factor from confidence score.
        Uses non-linear scaling for more natural voice modulation.
        
        Args:
            confidence (float): Confidence score (0.0 to 1.0)
            
        Returns:
            float: Intensity factor (0.3 to 1.0)
        """
        # Ensure confidence is in valid range
        confidence = max(0.0, min(1.0, confidence))
        
        # Use square root for non-linear scaling
        # This makes the effect more noticeable at higher confidence levels
        # Minimum 0.3 to always apply some effect
        return 0.3 + 0.7 * math.sqrt(confidence)
    
    def _scale_rate(self, base_rate, intensity):
        """Scale rate multiplier based on intensity."""
        # For rates > 1.0 (faster), increase with intensity
        # For rates < 1.0 (slower), decrease with intensity
        if base_rate > 1.0:
            # Fast speech gets faster with more intensity
            return 1.0 + (base_rate - 1.0) * intensity
        elif base_rate < 1.0:
            # Slow speech gets slower with more intensity
            return 1.0 - (1.0 - base_rate) * intensity
        else:
            return 1.0
    
    def _scale_pitch(self, base_pitch, intensity):
        """Scale pitch offset based on intensity."""
        # Scale pitch changes proportionally to intensity
        return base_pitch * intensity
    
    def _scale_volume(self, base_volume, intensity):
        """Scale volume based on intensity."""
        # For quiet voices, get quieter with intensity
        # For loud voices, maintain or slightly increase
        if base_volume < 0.85:
            return 0.9 - (0.9 - base_volume) * intensity
        else:
            return min(1.0, base_volume + (1.0 - base_volume) * intensity * 0.5)
    
    def get_all_emotions_info(self):
        """Get information about all supported emotions."""
        return {
            emotion: {
                'rate_multiplier': params['rate_multiplier'],
                'pitch_offset': params['pitch_offset'],
                'volume': params['volume'],
                'description': params['description']
            }
            for emotion, params in self.EMOTION_MAPPINGS.items()
        }


if __name__ == "__main__":
    # Test the voice modulator
    modulator = VoiceModulator(enable_intensity_scaling=True)
    
    print("\n" + "="*60)
    print("VOICE MODULATION TESTS")
    print("="*60 + "\n")
    
    # Test different emotions with varying confidence
    test_cases = [
        ('joy', 0.9),
        ('joy', 0.5),
        ('sadness', 0.8),
        ('anger', 0.95),
        ('fear', 0.7),
        ('surprise', 0.85),
        ('neutral', 1.0)
    ]
    
    for emotion, confidence in test_cases:
        params = modulator.get_voice_parameters(emotion, confidence)
        print(f"Emotion: {emotion} (confidence: {confidence:.2f})")
        print(f"  Rate: {params['rate_multiplier']:.2f}x")
        print(f"  Pitch: {params['pitch_offset']:+d}")
        print(f"  Volume: {params['volume']:.2f}")
        print(f"  Description: {params['description']}")
        print("-" * 60)
    
    print("\n" + "="*60)
    print("ALL EMOTION MAPPINGS")
    print("="*60 + "\n")
    
    for emotion, info in modulator.get_all_emotions_info().items():
        print(f"{emotion.upper()}: {info['description']}")
        print(f"  Base rate: {info['rate_multiplier']:.2f}x, pitch: {info['pitch_offset']:+d}, volume: {info['volume']:.2f}")
