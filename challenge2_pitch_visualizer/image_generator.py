"""
Image Generator - Generates images from prompts
Integrates with AI image generation APIs or uses placeholder images.
"""
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import os

class ImageGenerator:
    """Generates images from text prompts."""
    
    def __init__(self, api_key=None, use_placeholder=True):
        """
        Initialize the image generator.
        
        Args:
            api_key (str): API key for image generation service (OpenAI DALL-E, etc.)
            use_placeholder (bool): Use placeholder images if True (for testing)
        """
        self.api_key = api_key
        self.use_placeholder = use_placeholder
        
        if api_key and not use_placeholder:
            print("Image generator initialized with API")
        else:
            print("Image generator initialized in placeholder mode")
    
    def generate_image(self, prompt, scene_number=1, width=512, height=512):
        """
        Generate an image from a prompt.
        
        Args:
            prompt (str): Text prompt for image generation
            scene_number (int): Scene number for labeling
            width (int): Image width in pixels
            height (int): Image height in pixels
            
        Returns:
            PIL.Image: Generated image
        """
        if self.use_placeholder or not self.api_key:
            return self._generate_placeholder_image(prompt, scene_number, width, height)
        else:
            return self._generate_with_api(prompt, width, height)
    
    def _generate_placeholder_image(self, prompt, scene_number, width, height):
        """
        Generate a placeholder image with scene information.
        Useful for testing without API costs.
        """
        # Create base image with gradient background
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Create gradient background
        for y in range(height):
            # Color gradient from light blue to light purple
            r = int(150 + (y / height) * 50)
            g = int(180 + (y / height) * 20)
            b = int(220 - (y / height) * 40)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add border
        border_width = 5
        draw.rectangle(
            [border_width, border_width, width-border_width, height-border_width],
            outline=(100, 100, 150),
            width=border_width
        )
        
        # Try to load a default font, fall back to default if not available
        try:
            title_font = ImageFont.truetype("arial.ttf", 32)
            text_font = ImageFont.truetype("arial.ttf", 16)
            small_font = ImageFont.truetype("arial.ttf", 12)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Add scene number
        scene_text = f"Scene {scene_number}"
        bbox = draw.textbbox((0, 0), scene_text, font=title_font)
        text_width = bbox[2] - bbox[0]
        text_x = (width - text_width) // 2
        draw.text((text_x, 50), scene_text, fill=(50, 50, 100), font=title_font)
        
        # Add prompt text (wrapped)
        prompt_preview = prompt[:100] + "..." if len(prompt) > 100 else prompt
        
        # Word wrap the prompt
        words = prompt_preview.split()
        lines = []
        current_line = []
        current_width = 0
        max_line_width = width - 80
        
        for word in words:
            bbox = draw.textbbox((0, 0), word + " ", font=text_font)
            word_width = bbox[2] - bbox[0]
            
            if current_width + word_width <= max_line_width:
                current_line.append(word)
                current_width += word_width
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw wrapped text
        y_position = 120
        for line in lines[:5]:  # Max 5 lines
            bbox = draw.textbbox((0, 0), line, font=text_font)
            line_width = bbox[2] - bbox[0]
            x_position = (width - line_width) // 2
            draw.text((x_position, y_position), line, fill=(70, 70, 120), font=text_font)
            y_position += 25
        
        # Add placeholder notice
        notice = "[Placeholder Image - Connect API for AI generation]"
        bbox = draw.textbbox((0, 0), notice, font=small_font)
        notice_width = bbox[2] - bbox[0]
        draw.text(
            ((width - notice_width) // 2, height - 40),
            notice,
            fill=(120, 120, 150),
            font=small_font
        )
        
        return img
    
    def _generate_with_api(self, prompt, width, height):
        """
        Generate image using DALL-E API or similar service.
        
        Note: This requires a valid API key and will incur costs.
        """
        # Example implementation for DALL-E (requires openai package and API key)
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=f"{width}x{height}",
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Download the image
            image_response = requests.get(image_url)
            img = Image.open(io.BytesIO(image_response.content))
            
            return img
        
        except Exception as e:
            print(f"API generation failed: {e}")
            print("Falling back to placeholder image")
            return self._generate_placeholder_image(prompt, 1, width, height)
    
    def generate_images_for_prompts(self, prompts, width=512, height=512):
        """
        Generate images for multiple prompts.
        
        Args:
            prompts (list): List of prompt dictionaries
            width (int): Image width
            height (int): Image height
            
        Returns:
            list: List of PIL.Image objects
        """
        images = []
        for prompt_dict in prompts:
            print(f"Generating image for scene {prompt_dict['scene_number']}...")
            img = self.generate_image(
                prompt_dict['prompt'],
                scene_number=prompt_dict['scene_number'],
                width=width,
                height=height
            )
            images.append({
                'scene_number': prompt_dict['scene_number'],
                'image': img,
                'prompt': prompt_dict['prompt']
            })
        return images


if __name__ == "__main__":
    # Test the image generator
    generator = ImageGenerator(use_placeholder=True)
    
    print("\n" + "="*60)
    print("IMAGE GENERATOR TEST")
    print("="*60 + "\n")
    
    test_prompts = [
        {
            'scene_number': 1,
            'prompt': 'Scene 1: A woman entering a dark warehouse with a flashlight',
            'original_text': 'Sarah walked into the warehouse...'
        },
        {
            'scene_number': 2,
            'prompt': 'Scene 2: Close-up of an old journal being discovered',
            'original_text': 'She found an old journal...'
        }
    ]
    
    images = generator.generate_images_for_prompts(test_prompts, width=512, height=512)
    
    print(f"\nGenerated {len(images)} images")
    
    # Save test images
    output_dir = "../outputs/storyboards"
    os.makedirs(output_dir, exist_ok=True)
    
    for img_data in images:
        filename = f"test_scene_{img_data['scene_number']}.png"
        filepath = os.path.join(output_dir, filename)
        img_data['image'].save(filepath)
        print(f"Saved: {filepath}")
