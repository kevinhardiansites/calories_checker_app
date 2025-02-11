import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-pro')  # Pastikan model ini mendukung analisis gambar
    try:
        # Mengirimkan input prompt dan gambar ke model
        response = model.generate_content([input_prompt] + image)
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

# Initialize Streamlit app frontend
st.set_page_config(page_title="Calories Checker App")

st.header("Calories Checker App")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the total calories")

input_prompt = """
Anda adalah seorang ahli konsultan diet saya, di mana Anda perlu melihat makanan dari gambar
dan menyebutkan kandungan nutrisinya berdasarkan kemungkinan rata-rata. Selain itu, berikan rincian kemungkinan rata-rata setiap item makanan dengan asupan nutrisi
dalam format berikut ini:

1. Item 1 - jumlah nutrisi
2. Item 2 - jumlah nutrisi
----
----
Tulis saja kandungan-kandungan yang anda mengerti dari gambar tersebut.
Anda tidak pelu menuliskan disclaimer di awal respon.
Terakhir, Anda juga dapat menyebutkan apakah makanan tersebut sehat atau tidak dan juga
sebutkan persentase pembagian rasio karbohidrat, lemak, serat, gula, protein, minyak, dan lainnya yang dibutuhkan dalam makanan kita.
"""

if submit:
    with st.spinner("Analyzing image..."):
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)
            st.header("The Response is")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
