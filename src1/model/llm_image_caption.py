import os
import google.generativeai as genai
from PIL import Image

# Best practice: Load your API key from an environment variable
# In your terminal, run: export GOOGLE_API_KEY="your_api_key"
def generate_image_caption(image_object: Image.Image) -> str:
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        # Pass the image object directly to the model
        response = model.generate_content(["Describe this image...", image_object])
        return response.text
    except Exception as e:
        print(f"Error generating caption: {e}")
        return "Could not generate a caption for this image."