"""
Storyboard Composer - Combines images into a cohesive storyboard
Creates multi-panel storyboards from generated images with captions.
"""
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

class StoryboardComposer:
    """Composes multiple images into a storyboard layout."""
    
    def __init__(self):
        """Initialize the storyboard composer."""
        print("Storyboard composer initialized")
    
    def create_storyboard(self, images, layout='grid', add_captions=True,
                         caption_height=80, spacing=20, title=None):
        """
        Create a storyboard from multiple images.
        
        Args:
            images (list): List of image dictionaries with 'image', 'scene_number', 'prompt'
            layout (str): Layout style ('grid', 'horizontal', 'vertical')
            add_captions (bool): Whether to add captions below each panel
            caption_height (int): Height of caption area in pixels
            spacing (int): Spacing between panels in pixels
            title (str): Optional title for the storyboard
            
        Returns:
            PIL.Image: Composed storyboard image
        """
        if not images:
            raise ValueError("No images provided for storyboard")
        
        num_images = len(images)
        
        # Calculate grid dimensions
        if layout == 'grid':
            cols = min(3, num_images)  # Max 3 columns
            rows = (num_images + cols - 1) // cols
        elif layout == 'horizontal':
            cols = num_images
            rows = 1
        elif layout == 'vertical':
            cols = 1
            rows = num_images
        else:
            cols = min(3, num_images)
            rows = (num_images + cols - 1) // cols
        
        # Get panel dimensions from first image
        panel_width = images[0]['image'].width
        panel_height = images[0]['image'].height
        
        # Add space for captions if needed
        if add_captions:
            total_panel_height = panel_height + caption_height
        else:
            total_panel_height = panel_height
        
        # Add title space if provided
        title_height = 80 if title else 0
        
        # Calculate storyboard dimensions
        storyboard_width = cols * panel_width + (cols + 1) * spacing
        storyboard_height = title_height + rows * total_panel_height + (rows + 1) * spacing
        
        # Create blank storyboard canvas
        storyboard = Image.new('RGB', (storyboard_width, storyboard_height), color='white')
        draw = ImageDraw.Draw(storyboard)
        
        # Try to load fonts
        try:
            title_font = ImageFont.truetype("arial.ttf", 36)
            caption_font = ImageFont.truetype("arial.ttf", 14)
            scene_font = ImageFont.truetype("arial.ttf", 18)
        except:
            title_font = ImageFont.load_default()
            caption_font = ImageFont.load_default()
            scene_font = ImageFont.load_default()
        
        # Add title if provided
        if title:
            bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = bbox[2] - bbox[0]
            title_x = (storyboard_width - title_width) // 2
            draw.text((title_x, 30), title, fill=(50, 50, 100), font=title_font)
        
        # Place images on the storyboard
        for i, img_data in enumerate(images):
            row = i // cols
            col = i % cols
            
            # Calculate position
            x = spacing + col * (panel_width + spacing)
            y = title_height + spacing + row * (total_panel_height + spacing)
            
            # Paste the image
            storyboard.paste(img_data['image'], (x, y))
            
            # Add caption if enabled
            if add_captions:
                caption_y = y + panel_height + 10
                
                # Scene number
                scene_text = f"Scene {img_data['scene_number']}"
                draw.text((x + 10, caption_y), scene_text, fill=(0, 0, 0), font=scene_font)
                
                # Caption text (truncated to fit)
                if 'original_text' in img_data:
                    caption_text = img_data['original_text']
                    if len(caption_text) > 80:
                        caption_text = caption_text[:77] + "..."
                    
                    # Word wrap
                    words = caption_text.split()
                    lines = []
                    current_line = []
                    max_width = panel_width - 20
                    
                    for word in words:
                        test_line = ' '.join(current_line + [word])
                        bbox = draw.textbbox((0, 0), test_line, font=caption_font)
                        line_width = bbox[2] - bbox[0]
                        
                        if line_width <= max_width:
                            current_line.append(word)
                        else:
                            if current_line:
                                lines.append(' '.join(current_line))
                            current_line = [word]
                    
                    if current_line:
                        lines.append(' '.join(current_line))
                    
                    # Draw lines (max 2)
                    for j, line in enumerate(lines[:2]):
                        draw.text(
                            (x + 10, caption_y + 25 + j * 18),
                            line,
                            fill=(80, 80, 80),
                            font=caption_font
                        )
        
        return storyboard
    
    def save_storyboard(self, storyboard, filename=None, output_dir="../outputs/storyboards"):
        """
        Save storyboard to file.
        
        Args:
            storyboard (PIL.Image): Storyboard image
            filename (str): Optional filename
            output_dir (str): Output directory
            
        Returns:
            str: Path to saved file
        """
        os.makedirs(output_dir, exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"storyboard_{timestamp}.png"
        
        filepath = os.path.join(output_dir, filename)
        storyboard.save(filepath, quality=95)
        
        print(f"Storyboard saved to: {filepath}")
        return filepath


if __name__ == "__main__":
    # Test the storyboard composer
    from image_generator import ImageGenerator
    
    print("\n" + "="*60)
    print("STORYBOARD COMPOSER TEST")
    print("="*60 + "\n")
    
    # Generate test images
    generator = ImageGenerator(use_placeholder=True)
    
    test_prompts = [
        {
            'scene_number': 1,
            'prompt': 'A woman entering a dark warehouse with a flashlight',
            'original_text': 'Sarah walked into the old abandoned warehouse, her flashlight cutting through the darkness.'
        },
        {
            'scene_number': 2,
            'prompt': 'A woman discovering an old journal behind dusty crates',
            'original_text': 'Behind the dusty crates, she discovered an old journal with yellowed pages.'
        },
        {
            'scene_number': 3,
            'prompt': 'Close-up of a woman reading an old journal, eyes wide with shock',
            'original_text': 'As she read the first entry, her eyes widened in shock. This journal belonged to her grandmother.'
        },
        {
            'scene_number': 4,
            'prompt': 'A determined woman holding a journal, looking resolute',
            'original_text': 'Sarah knew she had to uncover the truth about her grandmother disappearance.'
        }
    ]
    
    images = generator.generate_images_for_prompts(test_prompts, width=400, height=400)
    
    # Create composer
    composer = StoryboardComposer()
    
    # Test different layouts
    print("Creating grid layout storyboard...")
    storyboard_grid = composer.create_storyboard(
        images,
        layout='grid',
        add_captions=True,
        title="The Mystery of Grandmother's Journal"
    )
    composer.save_storyboard(storyboard_grid, "test_grid_storyboard.png")
    
    print("\nCreating horizontal layout storyboard...")
    storyboard_h = composer.create_storyboard(
        images,
        layout='horizontal',
        add_captions=True
    )
    composer.save_storyboard(storyboard_h, "test_horizontal_storyboard.png")
    
    print("\nStoryboard tests complete!")
