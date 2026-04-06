"""
The Pitch Visualizer - Web Application
FastAPI web interface for narrative-to-storyboard generation.
"""
from fastapi import FastAPI, Request, Form, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime
from text_analyzer import TextAnalyzer
from prompt_generator import PromptGenerator
from image_generator import ImageGenerator
from storyboard_composer import StoryboardComposer

app = FastAPI(title="The Pitch Visualizer", description="Narrative-to-Storyboard Generation")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Setup static files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup output directory
OUTPUT_DIR = "../outputs/storyboards"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize components (global, loaded once at startup)
text_analyzer = None
prompt_generator = None
image_generator = None
storyboard_composer = None


@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    global text_analyzer, prompt_generator, image_generator, storyboard_composer
    print("Initializing The Pitch Visualizer...")
    text_analyzer = TextAnalyzer()
    prompt_generator = PromptGenerator(style="storyboard, digital art, cinematic")
    image_generator = ImageGenerator(use_placeholder=True)
    storyboard_composer = StoryboardComposer()
    print("✅ All systems ready!")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def generate_storyboard(
    narrative: str = Form(...),
    max_scenes: int = Form(6),
    title: str = Form("Storyboard")
):
    """
    Generate storyboard from narrative text.
    
    Args:
        narrative: Input narrative text
        max_scenes: Maximum number of scenes
        title: Storyboard title
        
    Returns:
        JSON with storyboard information
    """
    try:
        # Segment narrative into scenes
        scenes = text_analyzer.segment_narrative(narrative, max_scenes=max_scenes)
        
        # Generate image prompts
        prompts = prompt_generator.generate_prompts_for_scenes(scenes)
        
        # Generate images
        images = image_generator.generate_images_for_prompts(prompts, width=400, height=400)
        
        # Compose storyboard
        storyboard = storyboard_composer.create_storyboard(
            images,
            layout='grid',
            add_captions=True,
            title=title or "Storyboard"
        )
        
        # Save storyboard
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"storyboard_{timestamp}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        storyboard.save(filepath)
        
        return {
            "success": True,
            "narrative": narrative,
            "num_scenes": len(scenes),
            "scenes": [
                {
                    "scene_number": s["scene_number"],
                    "text": s["text"]
                }
                for s in scenes
            ],
            "storyboard_file": filename,
            "title": title
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/storyboard/{filename}")
async def get_storyboard(filename: str):
    """Serve storyboard images."""
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/png")
    return {"error": "File not found"}, 404


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🖼  Starting The Pitch Visualizer Web Server")
    print("="*60 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8003)
