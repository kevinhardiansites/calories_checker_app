import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=api_key)

def get_gemini_response(image_data):
    try:
        # Create a new instance of the GenerativeModel with the supported Gemini model
        model = genai.GenerativeModel('gemini-1.5-pro')  # Use a supported model name
        # Pass the image data directly to the generate_content method
        response = model.generate_content(image_data)
        return response
    except Exception as e:
        st.error(f"An error occurred while generating content: {str(e)}")
        return None

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read file into bytes
        bytes_data = uploaded_file.getvalue()
        return {
            "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
            "data": bytes_data
        }
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app frontend
st.set_page_config(page_title="Calories Checker App")
st.header("Calories Checker App")

# File uploader for images
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the total calories")

# If submit button is clicked
if submit:
    if uploaded_file is not None:
        with st.spinner("Processing..."):
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(image_data)
            if response:
                st.header("The Response is")
                st.write(response)
    else:
        st.error("Please upload an image before submitting.")
