import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()  # loading all the env variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-pro')  # Menggunakan model gemini-1.5-flash
    try:
        response = model.generate_content([input_prompt, image[0]])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize streamlit app frontend
st.set_page_config(page_title="Calories Checker App")

st.header("Calories Checker App")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the total calories")

input_prompt = """
You are an expert in nutrition where you need to see the food items from the image
and calculate the total calories. Also, provide the details of every food item with calorie intake
in the following format:

1. Item 1 - no of calories
2. Item 2 - no of calories
----
----
Finally, you can also mention whether the food is healthy or not and also
mention the percentage split of the ratio of carbohydrates, fats, fibers, sugar, protein, oils, and other required in our diet.
"""

if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        st.header("The Response is")
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
