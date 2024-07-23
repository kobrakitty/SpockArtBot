# Step 1: Setup
import streamlit as st
import requests
from openai import OpenAI
from io import BytesIO, StringIO
import os

# Get your OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")  # Used in production
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY")) 

# Step 2: Main Page Title & Description
st.title('👽AI Spock Art Critique Bot🛸')
st.subheader('Hello! I critique art you share with me. Either enter a URL or upload an image and click SUBMIT. Your art and my critique will appear below. Have fun!', divider='rainbow')

# Step 3: Sidebar Title and Design Elements
st.sidebar.title("Try It Out🎨")
st.sidebar.image("grumpyspock_byglitterpileai.jpg")

# Step 4: Create form for user input 
with st.sidebar.form(key='input_form'):
    user_input = st.text_area("Enter Your Image URL Here")
    uploaded_file = st.file_uploader("Or upload an image file", type=["jpg", "jpeg", "png"])
    submit_button = st.form_submit_button(label='SUBMIT🚀')     
    
# Step 5: Definition and Function to analyze URL using OpenAI
def analyze_artwork_with_gpt4_vision(user_input):
    if not api_key:
        st.error("OpenAI API key is not set. Please set it in your environment variables.")
        return "OpenAI API key not set."
     
    # Instructions for the AI (adjust if needed)
    messages = [
        {"role": "system", "content": "You are Spock from the original Star Trek series from the 1960s. Your main purpose is to provide art critiques of images from the user. Your answers should be logical, concise, and devoid of emotional language. Maintain a formal tone, using precise vocabulary and structured sentences. Include scientific or analytical explanations where applicable. The critique should focus on aspects such as composition, use of color, technique, perspective, and thematic elements. You will avoid subjective language; instead, rely on objective observations and logical analysis. Ask clarifying questions if additional information is needed to provide a logical response."},
        {"role": "user", "content": f"Review the following image:\n{user_input}"}
    ]
    try:
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-4o Turbo",
            temperature=0  # Lower temperature for less random responses
        )
        
        # Extract the critique from the response
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {e}")
        return str(e)
                label="Download Critique",
                data=get_text_file(critique_result).read(),  # Convert buffer to string
                file_name="critique.txt",
                mime="text/plain"
            )

# Step 5: Definition and Function to analyze UPLOAD using OpenAI
def analyze_artwork_with_gpt4_vision(uploaded_file):
    if not api_key:
        st.error("OpenAI API key is not set. Please set it in your environment variables.")
        return "OpenAI API key not set."
     
    # Instructions for the AI (adjust if needed)
    messages = [
        {"role": "system", "content": "You are Spock from the original Star Trek series from the 1960s. Your main purpose is to provide art critiques of images from the user. Your answers should be logical, concise, and devoid of emotional language. Maintain a formal tone, using precise vocabulary and structured sentences. Include scientific or analytical explanations where applicable. The critique should focus on aspects such as composition, use of color, technique, perspective, and thematic elements. You will avoid subjective language; instead, rely on objective observations and logical analysis. Ask clarifying questions if additional information is needed to provide a logical response."},
        {"role": "user", "content": f"Review the following image:\n{uploaded_file}"}
    ]
    try:
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-4o Turbo",
            temperature=0  # Lower temperature for less random responses
        )
        
        # Extract the critique from the response
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {e}")
        return str(e)
                label="Download Critique",
                data=get_text_file(critique_result).read(),  # Convert buffer to string
                file_name="critique.txt",
                mime="text/plain"
            )

# Helper function to create a text file for download
def get_text_file(content):
    buffer = StringIO()
    buffer.write(content)
    buffer.seek(0)
    return buffer

# Function to handle the submission process
def handle_submission(image_file):
    with st.spinner('🌟Critiquing...'):
        critique_result = analyze_artwork_with_gpt4_vision(image_file)
        st.markdown("### Spock Says...")
        st.write(critique_result)
        
        st.download_button(
            label="Download Critique",
            data=get_text_file(critique_result),  # Use buffer directly
            file_name="critique.txt",
            mime="text/plain"
        )

# Intructions
    if submit_button and user_input: 
        # Fetch the image from URL and convert it to a BytesIO object
        response = requests.get(user_input)
        image_file_URL = BytesIO(response.content)
        st.image(user_input, caption='Your Image', use_column_width=True)
        with st.spinner('🌟Critiquing...'):
            critique_result = analyze_artwork_with_gpt4_vision(image_file_URL)
            st.markdown("### Spock Says...")
            st.write(critique_result)
            
            # Add a download button for text
            def get_text_file(content):
                buffer = StringIO()
                buffer.write(content)
                buffer.seek(0)
                return buffer

            st.download_button(
                label="Download Critique",
                data=get_text_file(critique_result),  # Use buffer directly
                file_name="critique.txt",
                mime="text/plain"
            )
    
    elif submit_button and uploaded_file:
        # Read the uploaded file
        image_file_upload = BytesIO(uploaded_file.getvalue())
        st.image(uploaded_file, caption='Your Image', use_column_width=True)
        
            with st.spinner('🌟Critiquing...'):
            critique_result = analyze_artwork_with_gpt4_vision(image_file_upload)
            st.markdown("### Spock Says...")
            st.write(critique_result)
            
            # Add a download button for text
            def get_text_file(content):
                buffer = StringIO()
                buffer.write(content)
                buffer.seek(0)
                return buffer

            st.download_button(
                label="Download Critique",
                data=get_text_file(critique_result),  # Use buffer directly
                file_name="critique.txt",
                mime="text/plain"
            )

    else:
        st.error("No image provided.")
        image_file_upload = None
