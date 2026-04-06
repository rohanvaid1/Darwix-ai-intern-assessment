# The Pitch Visualizer 🖼

**Narrative-to-Storyboard Generation System**

Automatically convert narrative text into visual storyboards using AI-powered scene segmentation and image generation.

## Overview

The Pitch Visualizer transforms written narratives into compelling visual storyboards. It analyzes text, identifies key moments, generates descriptive prompts, and composes a multi-panel storyboard - automating a traditionally manual and time-consuming creative process.

## Features

✅ **Text Segmentation**: Intelligently breaks narratives into logical scenes  
✅ **Key Element Extraction**: Identifies characters, actions, settings, and emotions  
✅ **Prompt Generation**: Creates detailed, descriptive prompts for each scene  
✅ **Image Generation**: Supports AI image generation APIs or placeholder mode  
✅ **Storyboard Composition**: Assembles images into professional multi-panel layouts  
✅ **Multiple Layouts**: Grid, horizontal, and vertical arrangements  
✅ **Caption Support**: Automatic scene numbering and text captions

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Navigate to the project directory:**
   ```bash
   cd challenge2_pitch_visualizer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data:**
   ```bash
   python -m textblob.download_corpora
   python -c "import nltk; nltk.download('averaged_perceptron_tagger_eng')"
   ```

## Usage

### Command-Line Interface

1. **With direct text:**
   ```bash
   python pitch_visualizer_cli.py --text "Your narrative here..." --scenes 6 --title "My Story"
   ```

2. **From a text file:**
   ```bash
   python pitch_visualizer_cli.py --file story.txt --scenes 4 --title "Adventure"
   ```

3. **Interactive mode:**
   ```bash
   python pitch_visualizer_cli.py
   ```
   Then enter your narrative and type `END` when finished.

4. **With AI image generation (requires API key):**
   ```bash
   python pitch_visualizer_cli.py --text "Your story..." --api-key "your-openai-key"
   ```

### Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--text` | Narrative text to visualize | Interactive mode |
| `--file` | Path to text file | None |
| `--scenes` | Maximum number of scenes | 6 |
| `--title` | Storyboard title | "Storyboard" |
| `--api-key` | OpenAI API key for DALL-E | Placeholder mode |

### Output

- Storyboards are saved to `../outputs/storyboards/`
- Filenames include timestamp: `storyboard_20260406_123456.png`
- Individual scene images are also saved

## Example

**Input Narrative:**
```
Sarah walked into the old abandoned warehouse, her flashlight cutting through 
the darkness. Suddenly, she heard a noise from the corner. Behind the dusty 
crates, she discovered an old journal. This journal belonged to her grandmother 
who had disappeared 20 years ago. Sarah knew she had to uncover the truth.
```

**Output:** A 4-panel storyboard with:
- Scene 1: Woman entering dark warehouse with flashlight
- Scene 2: Reacting to mysterious noise
- Scene 3: Discovering the journal
- Scene 4: Determined expression, holding the journal

## Design Decisions

### Text Segmentation Strategy
- **Sentence-based splitting**: Uses NLTK for accurate sentence tokenization
- **Scene boundaries**: Detects transitions ("suddenly", "meanwhile", "then")
- **Adaptive grouping**: Adjusts sentences per scene based on total length
- **Maximum scenes**: Configurable limit to control storyboard size

### Prompt Generation
- **Multi-component prompts**: Combines scene description, key elements, mood, and style
- **Sentiment analysis**: Maps emotional tone to visual atmosphere
- **Consistency markers**: Adds instructions for maintaining character/style across scenes
- **Quality descriptors**: Includes "high quality, detailed, cinematic composition"

### Image Generation Modes
1. **Placeholder Mode** (default):
   - Generates gradient backgrounds with scene info
   - Perfect for testing and demo without API costs
   - Clearly labeled as placeholders

2. **API Mode** (with key):
   - Integrates with DALL-E 3 for photorealistic images
   - Falls back to placeholder if API fails
   - Automatically downloads and caches images

### Storyboard Layout
- **Grid layout**: Best for 4-9 scenes (2-3 columns)
- **Horizontal**: Ideal for timeline narratives (1 row)
- **Vertical**: Story progression top to bottom (1 column)
- **Spacing**: 20px between panels for clean presentation
- **Captions**: 2-line text under each panel with scene number

## Project Structure

```
challenge2_pitch_visualizer/
├── pitch_visualizer_cli.py    # Command-line interface
├── text_analyzer.py           # Text segmentation module
├── prompt_generator.py        # Image prompt creation
├── image_generator.py         # AI image generation
├── storyboard_composer.py     # Layout and composition
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## API Integration

### OpenAI DALL-E 3

To use real AI image generation:

1. Get an API key from [OpenAI](https://platform.openai.com/)
2. Pass it via command line: `--api-key "sk-..."`
3. Or set environment variable: `export OPENAI_API_KEY="sk-..."`

**Note:** API usage incurs costs ($0.04-0.08 per image for DALL-E 3)

### Alternative APIs

The `image_generator.py` module can be extended to support:
- Stability AI (Stable Diffusion)
- Midjourney API
- Azure Computer Vision
- Local Stable Diffusion models

## Technical Requirements Met

✅ **Text Input**: CLI and file input supported  
✅ **Text Segmentation**: Intelligent scene detection and grouping  
✅ **Key Element Extraction**: NLP-based analysis of characters, actions, settings  
✅ **Prompt Generation**: Detailed, descriptive prompts with consistency markers  
✅ **Image Generation**: Placeholder mode + API integration ready  
✅ **Multi-Panel Storyboard**: Grid, horizontal, and vertical layouts  
✅ **Visual Output**: High-quality PNG files with captions

## Future Enhancements

- 🎨 Style customization (cartoon, realistic, sketch, etc.)
- 👥 Character consistency across scenes
- 🎬 Animation and transitions
- 📊 Scene importance weighting
- 🌍 Multi-language support
- ☁️ Web interface for easier access
- 📤 Export to PowerPoint/PDF

## Troubleshooting

**"MissingCorpusError" or NLTK data errors:**
```bash
python -m textblob.download_corpora
python -c "import nltk; nltk.download('averaged_perceptron_tagger_eng')"
```

**API generation fails:**
- Check API key validity
- Verify internet connection
- System falls back to placeholder mode automatically

**Low-quality storyboards:**
- Use `--scenes` parameter to control scene count (4-6 recommended)
- Provide more detailed narrative text
- Use API mode instead of placeholder for better visuals

## License

MIT License - Feel free to use and modify!

## Author

Created as part of the Darwix AI Intern Assessment Challenge.
