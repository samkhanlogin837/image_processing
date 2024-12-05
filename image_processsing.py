# import streamlit as st
# from PIL import Image
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os

# # Load environment variablescdcd
# load_dotenv()

# # Configure Google Gemini API with your API key
# api_key = os.getenv("AIzaSyCVF3wYGalMZHBw1YrjfwHiXg9NYe9dojM")  # Store API key in `.env` file for security
# genai.configure(api_key=api_key)

# # Initialize Gemini Model
# try:
#     model = genai.GenerativeModel("gemini-1.5-flash")
# except Exception as e:
#     st.error(f"Failed to initialize Gemini model: {e}")
#     st.stop()

# # Function to process image input
# def input_image_details(file):
#     mime_type = "image/png" if file.name.lower().endswith('.png') else "image/jpeg"
#     return [{"mime_type": mime_type, "data": file.read()}]

# # Function to get the Gemini response
# def get_gemini_response(input_prompt, image_data, prompt=""):
#     try:
#         response = model.generate_content([input_prompt, image_data[0], prompt])
#         return response.text
#     except Exception as e:
#         st.error(f"Error while generating content: {e}")
#         return None

# # Streamlit App Interface
# st.title("Food Image Analysis with Google Gemini")
# st.write("Upload an image of food, and the app will analyze it using the Gemini API.")

# uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

# if uploaded_file:
#     # Display uploaded image
#     st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
#     # Process the uploaded image
#     try:
#         image_data = input_image_details(uploaded_file)
        
#         # Get response from Gemini
#         st.write("Analyzing the image...")
#         input_prompt = "Identify the food items in the image and provide their names and locations."
#         response = get_gemini_response(input_prompt, image_data)
        
#         if response:
#             st.success("Analysis Complete!")
#             st.write("### Food Scan Report:")
#             st.write(response)
#         else:
#             st.error("Failed to get a response from the Gemini API.")
#     except Exception as e:
#         st.error(f"Error processing the image: {e}")
# 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

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables
load_dotenv()

# Configure Google Gemini API with your API key
api_key = os.getenv("AIzaSyCVF3wYGalMZHBw1YrjfwHiXg9NYe9dojM")
genai.configure(api_key=api_key)

# Initialize FastAPI app
app = FastAPI()

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        # Determine MIME type
        mime_type = "image/png" if file.filename.lower().endswith(".png") else "image/jpeg"
        image_data = {"mime_type": mime_type, "data": file.file.read()}

        # Set up prompt
        input_prompt = "Identify the food items in the image and provide their names and locations."

        # Initialize Gemini Model and get a response
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content([input_prompt, image_data])
        
        return JSONResponse(content={"status": "success", "analysis": response.text}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
