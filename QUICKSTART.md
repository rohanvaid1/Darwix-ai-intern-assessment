# Quick Start Guide

This guide helps you get started with both challenges immediately.

## Challenge 1: The Empathy Engine 🎙

### Installation
```bash
cd challenge1_empathy_engine
pip install -r requirements.txt
python -m textblob.download_corpora
```

### Try It Now
```bash
# Test with a happy message
python empathy_engine_cli.py "I am so excited and happy about this amazing news!"

# Test with a sad message
python empathy_engine_cli.py "I feel disappointed and sad about what happened."

# Test with an angry message
python empathy_engine_cli.py "This is absolutely frustrating and unacceptable!"
```

### Start Web Interface
```bash
python app.py
```
Then open: http://localhost:8000

---

## Challenge 2: The Pitch Visualizer 🖼

### Installation
```bash
cd challenge2_pitch_visualizer
pip install -r requirements.txt
python -m textblob.download_corpora
python -c "import nltk; nltk.download('averaged_perceptron_tagger_eng')"
```

### Try It Now
```bash
# Example 1: Mystery story
python pitch_visualizer_cli.py --text "Sarah walked into the old abandoned warehouse, her flashlight cutting through the darkness. Suddenly, she heard a noise from the corner. Behind the dusty crates, she discovered an old journal. This journal belonged to her grandmother who had disappeared 20 years ago. Sarah knew she had to uncover the truth." --scenes 5 --title "The Mystery Warehouse"

# Example 2: Adventure story
python pitch_visualizer_cli.py --text "The brave explorer entered the ancient temple. Golden artifacts lined the dusty shelves. A mysterious inscription caught his attention. He carefully translated the ancient text. The secret of the lost civilization was finally revealed." --scenes 5 --title "Temple Discovery"

# Example 3: From a file
# Create a file called story.txt with your narrative, then:
python pitch_visualizer_cli.py --file story.txt --scenes 6
```

---

## Output Locations

### Challenge 1 - Audio Files
- Location: `outputs/audio/`
- Format: `.wav` files
- Naming: `empathy_engine_{emotion}_{timestamp}.wav`

### Challenge 2 - Storyboards
- Location: `outputs/storyboards/`
- Format: `.png` files
- Naming: `storyboard_{timestamp}.png`

---

## Troubleshooting

### Error: "MissingCorpusError"
Run: `python -m textblob.download_corpora`

### Error: "averaged_perceptron_tagger_eng not found"
Run: `python -c "import nltk; nltk.download('averaged_perceptron_tagger_eng')"`

### Audio not playing (Challenge 1)
- Check that output directory exists: `outputs/audio/`
- Verify `.wav` file was created
- Try playing the file with your system's default audio player

### Storyboard not generated (Challenge 2)
- Check that output directory exists: `outputs/storyboards/`
- Verify Pillow (PIL) is installed: `pip install pillow`
- Check for error messages in console

---

## Tips for Best Results

### Challenge 1: The Empathy Engine
- Use emotionally expressive text for better modulation
- Include exclamation marks or question marks for intensity
- Try contrasting emotions to hear the difference
- Sentences with 10-50 words work best

### Challenge 2: The Pitch Visualizer
- Narratives with 3-8 sentences work best
- Include descriptive language (adjectives, vivid verbs)
- Mention characters, settings, and actions clearly
- 4-6 scenes is the sweet spot for visual balance

---

## Example Test Commands

```bash
# Challenge 1: Test all emotions
cd challenge1_empathy_engine
python empathy_engine_cli.py "I am so happy and excited!"  # Joy
python empathy_engine_cli.py "This is terrible and makes me angry."  # Anger
python empathy_engine_cli.py "I feel sad and disappointed."  # Sadness
python empathy_engine_cli.py "Wow! I can't believe this!"  # Surprise
python empathy_engine_cli.py "I'm worried and scared."  # Fear

# Challenge 2: Test different narrative styles
cd challenge2_pitch_visualizer
python pitch_visualizer_cli.py --text "A detective investigated the crime scene. She found a crucial clue. The evidence pointed to an unexpected suspect. She made the arrest." --scenes 4 --title "Detective Story"
```

---

Enjoy exploring the applications! 🚀
