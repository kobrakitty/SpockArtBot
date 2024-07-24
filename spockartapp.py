# Step 1: Setup
import base64
import streamlit as st
from openai import OpenAI
import os
from io import BytesIO
from PIL import Image

# Get your OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")  # Used in production

# Initialize the client with your API key
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")  # Ensure your API key is set in the environment variables
)

# Step 2: Main Page Title & Description
st.title('👽AI Spock Art Critique Bot🛸')
st.subheader('Hello, I critique art as Spock. Share an image URL in the field to the left or upload and your image and my critique will appear below. Have fun!', divider='rainbow')

# Step 3: Sidebar Title and Design Elements
st.sidebar.title("Try It Out🎨")
st.sidebar.image("grumpyspock_byglitterpileai.jpg")

# Step 4: Create form for user input 
with st.sidebar.form(key='input_form'):
    user_input = st.text_area("Enter Your Image URL Here")
    uploaded_file = st.file_uploader("Or upload an image file", type=["jpg", "jpeg", "png"])
    submit_button = st.form_submit_button(label='SUBMIT🚀')

def encode_image(image_file):
    # Open the image using Pillow
    img = Image.open(image_file)
    
    # Convert to RGB if it's not
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    # Resize if the image is too large
    max_size = (1024, 1024)  # OpenAI's max size
    img.thumbnail(max_size, Image.LANCZOS)
    
    # Save the image to a bytes buffer
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    
    # Encode the image
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def analyze_artwork_with_gpt4_vision(image_input):
    if not api_key:
        st.error("OpenAI API key is not set. Please set it in your environment variables.")
        return "OpenAI API key not set."
    
    client = OpenAI(api_key=api_key)
    
    try:
        if isinstance(image_input, str):  # It's a URL
            image_content = image_input
        else:  # It's an uploaded file
            image_content = f"data:image/jpeg;base64,{encode_image(image_input)}"
        
        messages = [
            {"role": "system", "content": "You are Spock from the original Star Trek series from the 1960s. Your main purpose is to provide art critiques of images from the user. Your answers should be logical, concise, and devoid of emotional language. Maintain a formal tone, using precise vocabulary and structured sentences. Include scientific or analytical explanations where applicable. The critique should focus on aspects such as composition, use of color, technique, perspective, and thematic elements. You will avoid subjective language; instead, rely on objective observations and logical analysis. Ask clarifying questions if additional information is needed to provide a logical response."},
            {"role": "user", "content": [{"type": "image", "image": image_content}, "Analyze this image."]}
        ]
        
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=300
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {e}")
        return str(e)
