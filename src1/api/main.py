from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import run_in_threadpool
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os
from pathlib import Path  # Import Path
from src1.model.llm_image_caption import generate_image_caption
import io
import google.generativeai as genai
from pathlib import Path
app = FastAPI()
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("FATAL ERROR: GOOGLE_API_KEY environment variable not set.")
    # In a real app, you might want to exit or handle this more gracefully
    exit()
# --- Build robust, portable paths ---
SCRIPT_DIR = Path(__file__).parent 
PROJECT_ROOT = SCRIPT_DIR.parent.parent
MODEL_PATH = os.path.join(PROJECT_ROOT,"models//transfer_model_best.h5")
HTML_PATH = os.path.join(PROJECT_ROOT,"frontend//index.html")
# Load model and define labels
model = load_model(MODEL_PATH)
class_names = ["buildings", "forest", "glacier", "mountain", "sea", "street"]

@app.get("/", response_class=HTMLResponse)
async def read_index():
    # Use the robustly defined HTML_PATH
    html_file_path = Path(HTML_PATH)
    if not html_file_path.is_file():
        return HTMLResponse(content="Index file not found.", status_code=404)
    with html_file_path.open("r", encoding="utf-8") as f:
        html_content = await run_in_threadpool(f.read)
    return HTMLResponse(content=html_content, status_code=200)
@app.post("/predict")
async def predict(file: UploadFile):
    # 2. Read the entire file content into an in-memory variable
    image_bytes = await file.read()
    
    # Create an in-memory binary stream (like a temporary file in RAM)
    image_stream = io.BytesIO(image_bytes)

    # --- All operations now use the in-memory stream, not a file on disk ---

    # Preprocess for classification using the in-memory stream
    with Image.open(image_stream) as img:
        # We'll need this PIL image object again for the captioning
        img_for_caption = img.copy() 
        image_resized = img.resize((150, 150))
        image_array = np.array(image_resized) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

    # Model prediction
    prediction = model.predict(image_array)
    predicted_class = class_names[np.argmax(prediction)]
    
    # 3. Modify the caption function to accept the image object directly
    #    instead of a file path. This avoids reopening a file.
    caption = generate_image_caption(img_for_caption) 
    
    return {
        "prediction": predicted_class,
        "description": caption
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)