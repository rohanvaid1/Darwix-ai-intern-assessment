"""
Prompt Generator - Creates image generation prompts from scene descriptions
Converts text scenes into detailed, descriptive prompts for AI image generation.
"""

class PromptGenerator:
    """Generates detailed image prompts from scene analysis."""
    
    def __init__(self, style="digital art, storyboard style"):
        """
        Initialize the prompt generator.
        
        Args:
            style (str): Default art style to apply to all prompts
        """
        self.style = style
        self.mood_descriptors = {
            'positive': 'bright, vibrant, warm lighting, hopeful atmosphere',
            'negative': 'dark, moody, dramatic lighting, tense atmosphere',
            'neutral': 'balanced lighting, natural colors, calm atmosphere'
        }
    
    def generate_prompt(self, scene):
        """
        Generate a detailed image prompt from a scene.
        
        Args:
            scene (dict): Scene data with text and key_elements
            
        Returns:
            str: Detailed prompt for image generation
        """
        text = scene['text']
        elements = scene['key_elements']
        scene_number = scene['scene_number']
        
        # Determine mood from sentiment
        polarity = elements['sentiment_polarity']
        if polarity > 0.2:
            mood = 'positive'
        elif polarity < -0.2:
            mood = 'negative'
        else:
            mood = 'neutral'
        
        mood_desc = self.mood_descriptors[mood]
        
        # Build prompt components
        components = []
        
        # Main scene description (first 100 characters of text)
        main_desc = text[:150] + "..." if len(text) > 150 else text
        components.append(main_desc)
        
        # Add key elements
        if elements['nouns']:
            components.append(f"featuring {', '.join(elements['nouns'][:3])}")
        
        if elements['adjectives']:
            components.append(f"{', '.join(elements['adjectives'][:2])} scene")
        
        if elements['verbs']:
            action = elements['verbs'][0] if elements['verbs'] else "happening"
            components.append(f"action: {action}")
        
        # Add mood and style
        components.append(mood_desc)
        components.append(self.style)
        
        # Additional quality descriptors
        components.append("high quality, detailed, cinematic composition")
        
        # Combine into final prompt
        prompt = ", ".join(components)
        
        # Add scene number context
        prompt = f"Scene {scene_number}: {prompt}"
        
        return prompt
    
    def generate_prompts_for_scenes(self, scenes):
        """
        Generate prompts for multiple scenes.
        
        Args:
            scenes (list): List of scene dictionaries
            
        Returns:
            list: List of prompts, one for each scene
        """
        prompts = []
        for scene in scenes:
            prompt = self.generate_prompt(scene)
            prompts.append({
                'scene_number': scene['scene_number'],
                'prompt': prompt,
                'original_text': scene['text']
            })
        return prompts
    
    def enhance_prompt_with_consistency(self, prompts, character_names=None):
        """
        Enhance prompts to maintain consistency across scenes.
        
        Args:
            prompts (list): List of prompt dictionaries
            character_names (list): Optional list of character names to maintain
            
        Returns:
            list: Enhanced prompts with consistency markers
        """
        if not prompts:
            return prompts
        
        # Add consistency instructions
        consistency_note = "consistent art style throughout"
        
        if character_names:
            char_desc = f"maintain consistent appearance for characters: {', '.join(character_names)}"
            consistency_note += f", {char_desc}"
        
        for prompt_dict in prompts:
            prompt_dict['prompt'] = f"{prompt_dict['prompt']}, {consistency_note}"
        
        return prompts


if __name__ == "__main__":
    # Test the prompt generator
    generator = PromptGenerator()
    
    # Sample scene for testing
    sample_scene = {
        'scene_number': 1,
        'text': 'Sarah walked into the old abandoned warehouse, her flashlight cutting through the darkness.',
        'word_count': 14,
        'sentence_count': 1,
        'key_elements': {
            'nouns': ['Sarah', 'warehouse', 'flashlight', 'darkness'],
            'verbs': ['walked', 'cutting'],
            'adjectives': ['old', 'abandoned'],
            'sentiment_polarity': -0.2,
            'sentiment_subjectivity': 0.6
        }
    }
    
    print("\n" + "="*60)
    print("PROMPT GENERATOR TEST")
    print("="*60 + "\n")
    
    print(f"Original scene text:\n{sample_scene['text']}\n")
    print("="*60 + "\n")
    
    prompt = generator.generate_prompt(sample_scene)
    print(f"Generated prompt:\n{prompt}\n")
    print("="*60 + "\n")
    
    # Test multiple scenes
    sample_scenes = [
        sample_scene,
        {
            'scene_number': 2,
            'text': 'Behind the dusty crates, she discovered an old journal with yellowed pages.',
            'word_count': 12,
            'sentence_count': 1,
            'key_elements': {
                'nouns': ['crates', 'journal', 'pages'],
                'verbs': ['discovered'],
                'adjectives': ['dusty', 'old', 'yellowed'],
                'sentiment_polarity': 0.1,
                'sentiment_subjectivity': 0.7
            }
        }
    ]
    
    prompts = generator.generate_prompts_for_scenes(sample_scenes)
    print("Multiple scene prompts:")
    for p in prompts:
        print(f"\nScene {p['scene_number']}:")
        print(f"  Prompt: {p['prompt'][:150]}...")
