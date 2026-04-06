"""
Text Analyzer - Segments narrative into key scenes
Breaks down narrative text into logical segments for storyboard creation.
"""
import re
from textblob import TextBlob
import nltk

class TextAnalyzer:
    """Analyzes and segments narrative text into key moments/scenes."""
    
    def __init__(self):
        """Initialize the text analyzer."""
        print("Initializing text analyzer...")
        
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading NLTK data...")
            nltk.download('punkt', quiet=True)
        
        print("Text analyzer ready!")
    
    def segment_narrative(self, text, max_scenes=6):
        """
        Segment narrative text into key scenes/moments.
        
        Args:
            text (str): Input narrative text
            max_scenes (int): Maximum number of scenes to extract
            
        Returns:
            list: List of scene dictionaries with text and metadata
        """
        # Split into sentences
        sentences = self._split_into_sentences(text)
        
        if len(sentences) == 0:
            return []
        
        # Group sentences into scenes
        scenes = self._group_into_scenes(sentences, max_scenes)
        
        # Analyze each scene
        analyzed_scenes = []
        for i, scene_text in enumerate(scenes):
            analyzed_scenes.append({
                'scene_number': i + 1,
                'text': scene_text,
                'word_count': len(scene_text.split()),
                'sentence_count': len([s for s in sentences if s in scene_text]),
                'key_elements': self._extract_key_elements(scene_text)
            })
        
        return analyzed_scenes
    
    def _split_into_sentences(self, text):
        """Split text into sentences using NLTK."""
        # Clean the text
        text = text.strip()
        
        # Use NLTK to split into sentences
        sentences = nltk.sent_tokenize(text)
        
        # Clean up sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def _group_into_scenes(self, sentences, max_scenes):
        """Group sentences into logical scenes."""
        if len(sentences) <= max_scenes:
            # Each sentence is a scene
            return sentences
        
        # Calculate sentences per scene
        sentences_per_scene = max(1, len(sentences) // max_scenes)
        
        scenes = []
        current_scene = []
        
        for i, sentence in enumerate(sentences):
            current_scene.append(sentence)
            
            # Check if we should start a new scene
            if (len(current_scene) >= sentences_per_scene and 
                len(scenes) < max_scenes - 1) or \
               self._is_scene_boundary(sentence):
                scenes.append(' '.join(current_scene))
                current_scene = []
        
        # Add remaining sentences
        if current_scene:
            if scenes:
                # Append to last scene if it's short
                if len(current_scene) <= 2:
                    scenes[-1] += ' ' + ' '.join(current_scene)
                else:
                    scenes.append(' '.join(current_scene))
            else:
                scenes.append(' '.join(current_scene))
        
        return scenes[:max_scenes]
    
    def _is_scene_boundary(self, sentence):
        """Determine if sentence marks a scene boundary."""
        # Scene transition indicators
        transitions = [
            'later', 'meanwhile', 'next', 'then', 'after', 
            'suddenly', 'finally', 'eventually', 'soon'
        ]
        
        sentence_lower = sentence.lower()
        return any(transition in sentence_lower.split()[:3] for transition in transitions)
    
    def _extract_key_elements(self, text):
        """Extract key elements from scene text (characters, actions, settings)."""
        blob = TextBlob(text)
        
        # Extract nouns (potential characters/objects/settings)
        nouns = [word for word, tag in blob.tags if tag.startswith('NN')]
        
        # Extract verbs (actions)
        verbs = [word for word, tag in blob.tags if tag.startswith('VB')]
        
        # Extract adjectives (descriptors)
        adjectives = [word for word, tag in blob.tags if tag.startswith('JJ')]
        
        # Get sentiment
        sentiment = blob.sentiment
        
        return {
            'nouns': list(set(nouns))[:5],  # Top 5 unique nouns
            'verbs': list(set(verbs))[:3],  # Top 3 unique verbs
            'adjectives': list(set(adjectives))[:3],  # Top 3 unique adjectives
            'sentiment_polarity': sentiment.polarity,
            'sentiment_subjectivity': sentiment.subjectivity
        }


if __name__ == "__main__":
    # Test the text analyzer
    analyzer = TextAnalyzer()
    
    sample_narrative = """
    Sarah walked into the old abandoned warehouse, her flashlight cutting through the darkness. 
    Suddenly, she heard a noise from the corner. Her heart raced as she slowly approached. 
    Behind the dusty crates, she discovered an old journal. The pages were yellowed with age, 
    but the handwriting was clear. As she read the first entry, her eyes widened in shock. 
    This journal belonged to her grandmother, who had disappeared 20 years ago. 
    Sarah knew she had to uncover the truth.
    """
    
    print("\n" + "="*60)
    print("TEXT ANALYZER TEST")
    print("="*60 + "\n")
    
    print(f"Input narrative:\n{sample_narrative}\n")
    print("="*60 + "\n")
    
    scenes = analyzer.segment_narrative(sample_narrative, max_scenes=4)
    
    print(f"Extracted {len(scenes)} scenes:\n")
    for scene in scenes:
        print(f"Scene {scene['scene_number']}:")
        print(f"  Text: {scene['text'][:100]}...")
        print(f"  Words: {scene['word_count']}, Sentences: {scene['sentence_count']}")
        print(f"  Key nouns: {', '.join(scene['key_elements']['nouns'])}")
        print(f"  Key verbs: {', '.join(scene['key_elements']['verbs'])}")
        print(f"  Adjectives: {', '.join(scene['key_elements']['adjectives'])}")
        print(f"  Sentiment: {scene['key_elements']['sentiment_polarity']:.2f}")
        print("-" * 60)
