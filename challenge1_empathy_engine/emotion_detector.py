"""
Emotion Detection Module
Uses TextBlob for sentiment analysis and rule-based emotion classification.
"""
from textblob import TextBlob
import re

class EmotionDetector:
    """Detects emotions in text using sentiment analysis and keyword matching."""
    
    def __init__(self):
        """Initialize the emotion detector."""
        print("Loading emotion detection system...")
        
        # Keyword patterns for emotion detection
        self.emotion_keywords = {
            'joy': [
                'happy', 'excited', 'great', 'wonderful', 'amazing', 'excellent',
                'fantastic', 'delighted', 'joyful', 'pleased', 'glad', 'cheerful',
                'love', 'awesome', 'best', 'perfect', 'brilliant', 'yay', '!!'
            ],
            'sadness': [
                'sad', 'unhappy', 'depressed', 'disappointed', 'sorry', 'unfortunate',
                'regret', 'miss', 'lonely', 'miserable', 'heartbroken', 'crying',
                'terrible', 'awful', 'worst', 'bad', 'poor'
            ],
            'anger': [
                'angry', 'furious', 'mad', 'annoyed', 'irritated', 'frustrated',
                'outraged', 'hate', 'disgusted', 'rage', 'damn', 'stupid',
                'ridiculous', 'unacceptable', 'outrageous'
            ],
            'fear': [
                'scared', 'afraid', 'worried', 'anxious', 'nervous', 'terrified',
                'frightened', 'panic', 'concerned', 'uncertain', 'doubt', 'risky'
            ],
            'surprise': [
                'wow', 'surprised', 'shocked', 'amazed', 'astonished', 'unexpected',
                'unbelievable', 'incredible', 'omg', 'no way', 'really', 'what',
                'can\'t believe', '?!'
            ],
            'disgust': [
                'disgusting', 'gross', 'horrible', 'nasty', 'revolting', 'awful',
                'repulsive', 'sick', 'yuck', 'ew'
            ]
        }
        
        print("Emotion detection system loaded successfully!")
    
    def detect_emotion(self, text):
        """
        Detect the primary emotion and all emotion scores in the text.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: {
                'primary_emotion': str,
                'confidence': float,
                'all_emotions': dict
            }
        """
        if not text or not text.strip():
            return {
                'primary_emotion': 'neutral',
                'confidence': 1.0,
                'all_emotions': {'neutral': 1.0}
            }
        
        text_lower = text.lower()
        
        # Analyze sentiment using TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        # Calculate emotion scores based on keywords
        emotion_scores = {}
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = score
        
        # Determine primary emotion
        max_keyword_score = max(emotion_scores.values())
        
        if max_keyword_score > 0:
            # Use keyword-based detection
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = min(0.95, 0.6 + (max_keyword_score * 0.15))
        else:
            # Use sentiment-based detection
            if polarity > 0.3:
                primary_emotion = 'joy'
                confidence = 0.5 + (polarity * 0.4)
            elif polarity < -0.3:
                if subjectivity > 0.6:
                    primary_emotion = 'anger'
                else:
                    primary_emotion = 'sadness'
                confidence = 0.5 + (abs(polarity) * 0.4)
            else:
                primary_emotion = 'neutral'
                confidence = 0.7
        
        # Normalize scores for all emotions
        total = sum(emotion_scores.values()) + 1  # +1 for neutral
        all_emotions = {
            emotion: score / total
            for emotion, score in emotion_scores.items()
        }
        all_emotions['neutral'] = 1.0 / total
        
        # Boost the primary emotion score
        if primary_emotion != 'neutral':
            all_emotions[primary_emotion] = confidence
        
        return {
            'primary_emotion': primary_emotion,
            'confidence': confidence,
            'all_emotions': all_emotions,
            'sentiment': {
                'polarity': polarity,
                'subjectivity': subjectivity
            }
        }
    
    def get_emotion_intensity(self, text):
        """
        Get both the emotion type and its intensity.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            tuple: (emotion_name, intensity_score)
        """
        result = self.detect_emotion(text)
        return result['primary_emotion'], result['confidence']


if __name__ == "__main__":
    # Test the emotion detector
    detector = EmotionDetector()
    
    test_texts = [
        "I am so happy and excited about this amazing news!",
        "This is terrible and makes me very angry.",
        "I feel sad and disappointed about what happened.",
        "The meeting is scheduled for tomorrow at 3 PM.",
        "Wow! I can't believe this is happening!",
        "I'm worried and scared about the future."
    ]
    
    print("\n" + "="*60)
    print("EMOTION DETECTION TESTS")
    print("="*60 + "\n")
    
    for text in test_texts:
        result = detector.detect_emotion(text)
        print(f"Text: {text}")
        print(f"Primary Emotion: {result['primary_emotion']} (confidence: {result['confidence']:.2f})")
        print(f"Sentiment: polarity={result['sentiment']['polarity']:.2f}, subjectivity={result['sentiment']['subjectivity']:.2f}")
        top_emotions = sorted(result['all_emotions'].items(), key=lambda x: x[1], reverse=True)[:3]
        print(f"Top emotions: {', '.join([f'{k}: {v:.2f}' for k, v in top_emotions])}")
        print("-" * 60)
