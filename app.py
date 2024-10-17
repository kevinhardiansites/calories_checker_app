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

def get_gemini_response(input_prompt, image_data):
    try:
        # Create a new instance of the GenerativeModel with the supported Gemini model
        model = genai.GenerativeModel('gemini-1.5-pro')  # Use a supported model name
        response = model.generate_content([input_prompt, image_data])
        return response
    except Exception as e:
        st.error(f"An error occurred while generating content: {str(e)}")
        return None

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
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

input_prompt = """
You are an expert nutritionist. Analyze the food items from the image
and calculate the total calories. Provide the details of each food item with calorie intake
in the following format:

1. Item 1 - number of calories
2. Item 2 - number of calories
...
Finally, mention whether the food is healthy or not and provide the percentage split of the ratio of carbohydrates, fats, fibers, sugar, protein, oils, and other required nutrients in our diet.
"""

# If submit button is clicked
if submit:
    if uploaded_file is not None:
        with st.spinner("Processing..."):
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)
            if response:
                st.header("The Response is")
                st.write(response)
    else:
        st.error("Please upload an image before submitting.")
