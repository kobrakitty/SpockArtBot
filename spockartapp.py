# Step 1: Setup
import streamlit as st
from openai import OpenAI
import os
import io

# Get your OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")  # Used in production

# Create OpenAI client
client = OpenAI(api_key=api_key)

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

# Step 5: Definition and Function to analyze image using OpenAI
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
            model="gpt-4-turbo",
            temperature=0  # Lower temperature for less random responses
        )
        
        # Extract the critique from the response
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {e}")
        return str(e)

# Step 6: Handle form submission and display result
if submit_button:
    image_url = user_input if user_input else None
    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with open("temp_image", "wb") as f:
            f.write(uploaded_file.getbuffer())
        image_url = "temp_image"  # Set image_url to the temporary file path

    if image_url:
        with st.spinner('🌟Critiquing...'):
            critique_result = analyze_artwork_with_gpt4_vision(image_url) 
            # Display the image
            st.image(image_url, caption='Your Image', use_column_width=True)
            # Display the generated response
            st.markdown("### Spock Says...")
            st.write(critique_result)
            
            # Add a download button for text
            def get_text_file(content):
                buffer = io.StringIO()
                buffer.write(content)
                buffer.seek(0)
                return buffer

            st.download_button(
                label="Download Critique",
                data=get_text_file(critique_result).read(),  # Convert buffer to string
                file_name="critique.txt",
                mime="text/plain"
            )
