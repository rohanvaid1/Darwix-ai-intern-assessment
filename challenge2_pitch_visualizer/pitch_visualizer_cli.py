"""
The Pitch Visualizer - CLI Interface
Command-line interface for narrative-to-storyboard generation.
"""
import sys
from text_analyzer import TextAnalyzer
from prompt_generator import PromptGenerator
from image_generator import ImageGenerator
from storyboard_composer import StoryboardComposer

class PitchVisualizer:
    """Main application class for The Pitch Visualizer."""
    
    def __init__(self, api_key=None):
        """
        Initialize The Pitch Visualizer.
        
        Args:
            api_key (str): Optional API key for AI image generation
        """
        print("\n" + "="*60)
        print("🖼  THE PITCH VISUALIZER - Narrative to Storyboard")
        print("="*60 + "\n")
        
        # Initialize components
        self.text_analyzer = TextAnalyzer()
        self.prompt_generator = PromptGenerator(style="storyboard, digital art, cinematic")
        self.image_generator = ImageGenerator(api_key=api_key, use_placeholder=(api_key is None))
        self.storyboard_composer = StoryboardComposer()
        
        print("\n✅ All systems ready!\n")
    
    def process_narrative(self, narrative, max_scenes=6, title=None):
        """
        Process narrative text and generate storyboard.
        
        Args:
            narrative (str): Input narrative text
            max_scenes (int): Maximum number of scenes to generate
            title (str): Optional title for the storyboard
            
        Returns:
            dict: Processing results including storyboard path
        """
        print(f"📝 Input narrative ({len(narrative)} characters):\n")
        print(narrative[:200] + "..." if len(narrative) > 200 else narrative)
        print("\n" + "="*60 + "\n")
        
        # Step 1: Segment narrative into scenes
        print("🔍 Step 1: Analyzing and segmenting narrative...")
        scenes = self.text_analyzer.segment_narrative(narrative, max_scenes=max_scenes)
        print(f"   ✅ Extracted {len(scenes)} scenes\n")
        
        for scene in scenes:
            print(f"   Scene {scene['scene_number']}: {scene['text'][:60]}...")
        
        print("\n" + "="*60 + "\n")
        
        # Step 2: Generate image prompts
        print("🎨 Step 2: Generating image prompts...")
        prompts = self.prompt_generator.generate_prompts_for_scenes(scenes)
        print(f"   ✅ Created {len(prompts)} detailed prompts\n")
        
        for prompt in prompts:
            print(f"   Scene {prompt['scene_number']}:")
            print(f"     {prompt['prompt'][:80]}...")
        
        print("\n" + "="*60 + "\n")
        
        # Step 3: Generate images
        print("🖼  Step 3: Generating images...")
        images = self.image_generator.generate_images_for_prompts(prompts, width=512, height=512)
        print(f"   ✅ Generated {len(images)} images\n")
        
        # Step 4: Compose storyboard
        print("📋 Step 4: Composing storyboard...")
        storyboard = self.storyboard_composer.create_storyboard(
            images,
            layout='grid',
            add_captions=True,
            title=title or "Storyboard"
        )
        
        # Save storyboard
        storyboard_path = self.storyboard_composer.save_storyboard(storyboard)
        print(f"   ✅ Storyboard created!\n")
        
        print("="*60)
        print(f"✅ Complete! Storyboard saved to:\n   {storyboard_path}")
        print("="*60 + "\n")
        
        return {
            'narrative': narrative,
            'scenes': scenes,
            'prompts': prompts,
            'images': images,
            'storyboard_path': storyboard_path
        }


def main():
    """Main CLI function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='The Pitch Visualizer - Convert narratives to storyboards')
    parser.add_argument('--text', type=str, help='Narrative text to visualize')
    parser.add_argument('--file', type=str, help='Path to text file containing narrative')
    parser.add_argument('--scenes', type=int, default=6, help='Maximum number of scenes (default: 6)')
    parser.add_argument('--title', type=str, help='Storyboard title')
    parser.add_argument('--api-key', type=str, help='API key for AI image generation (optional)')
    
    args = parser.parse_args()
    
    # Get narrative text
    narrative = None
    if args.text:
        narrative = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                narrative = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    
    if not narrative:
        # Interactive mode
        print("="*60)
        print("Interactive Mode - Enter your narrative")
        print("(Type END on a new line when finished)")
        print("="*60 + "\n")
        
        lines = []
        while True:
            try:
                line = input()
                if line.strip().upper() == 'END':
                    break
                lines.append(line)
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)
        
        narrative = '\n'.join(lines)
    
    if not narrative or not narrative.strip():
        print("Error: No narrative provided!")
        sys.exit(1)
    
    # Initialize and process
    visualizer = PitchVisualizer(api_key=args.api_key)
    visualizer.process_narrative(narrative, max_scenes=args.scenes, title=args.title)


if __name__ == "__main__":
    main()
