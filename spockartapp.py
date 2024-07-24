# Step 1: Setup
import streamlit as st
from openai import OpenAI
import os
import io

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

# Step 5: Definition and Function to analyze image using OpenAI
def analyze_artwork_with_gpt4_vision(image_input):
    if not api_key:
        st.error("OpenAI API key is not set. Please set it in your environment variables.")
        return "OpenAI API key not set."
    
    client = OpenAI(api_key=api_key)
    
    messages = [
        {"role": "system", "content": "You are Spock from the original Star Trek series from the 1960s. Your main purpose is to provide art critiques of images from the user. Your answers should be logical, concise, and devoid of emotional language. Maintain a formal tone, using precise vocabulary and structured sentences. Include scientific or analytical explanations where applicable. The critique should focus on aspects such as composition, use of color, technique, perspective, and thematic elements. You will avoid subjective language; instead, rely on objective observations and logical analysis. Ask clarifying questions if additional information is needed to provide a logical response."},
        {"role": "user", "content": [{"type": "image", "image": image_input}, "Analyze this image."]}
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=300
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {e}")
        return str(e)

# Step 6: Handle form submission and display result
if submit_button:
    image_input = None
    if user_input:
        image_input = user_input  # This is the URL
    elif uploaded_file is not None:
        image_input = uploaded_file.getvalue()  # This is the file content
    
    if image_input:
        with st.spinner('🌟Critiquing...'):
            critique_result = analyze_artwork_with_gpt4_vision(image_input)
            
            # Display the image
            if isinstance(image_input, str):  # If it's a URL
                st.image(image_input, caption='Your Image', use_column_width=True)
            else:  # If it's an uploaded file
                st.image(image_input, caption='Your Image', use_column_width=True)
            
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
                data=get_text_file(critique_result).read(),
                file_name="critique.txt",
                mime="text/plain"
            )
    else:
        st.error("Please provide either an image URL or upload an image file.")
