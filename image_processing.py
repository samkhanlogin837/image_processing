from fastapi import FastAPI, File, UploadFile
from typing import List
import google.generativeai as genai
from fastapi.responses import JSONResponse
import io
from PIL import Image

# Configure Google Gemini API with your API key
genai.configure(api_key="AIzaSyCVF3wYGalMZHBw1YrjfwHiXg9NYe9dojM")  # Replace with your actual API key
# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()

def input_image_details(file: UploadFile):
    try:
        # Read image as bytes
        image_data = file.file.read()

        # Determine the MIME type based on file extension
        if file.filename.lower().endswith('.png'):
            mime_type = "image/png"
        else:
            mime_type = "image/jpeg"

        image_parts = [
            {
                "mime_type": mime_type,
                "data": image_data
            }
        ]
        return image_parts
    except Exception as e:
        raise Exception(f"Error processing the image: {e}")

def get_gemini_response(input_prompt: str, image_data: List[dict], prompt: str) -> str:
    try:
        response = model.generate_content([input_prompt, image_data[0], prompt])
        return response.text
    except Exception as e:
        print(f"Error while generating content: {e}")
        return None

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")  # Print file name to confirm it's received
    try:
        image_data = input_image_details(file)

        # Call Gemini API with the prompt
        input_prompt = "Identify the food items in the image and provide their names and locations."
        response = get_gemini_response(input_prompt, image_data, "")
        
        if response:
            return JSONResponse(content={"status": "success", "message": response})
        else:
            return JSONResponse(content={"status": "error", "message": "Failed to get response from Gemini API."}, status_code=500)
    
    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=400)
