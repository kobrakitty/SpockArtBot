# Step 1: Setup
import streamlit as st
from openai import OpenAI
import os

# Get your OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")  # Used in production

# Initialize the client with your API key
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")  # Ensure your API key is set in the environment variables
)

# Step 2: Main Page Title & Description
st.title('👽AI Spock Art Critique Bot🛸')
st.subheader('I am AI Spock Art Critique Bot. I critique art you share with me using an image URL. Your image and my critique will appear below. Have fun!', divider='rainbow')

# Step 3: Sidebar Title and Design Elements
st.sidebar.title("Try It Out🎨")
st.sidebar.image("grumpyspock_byglitterpileai.jpg")

# Step 4: Create form for user input 
with st.sidebar.form(key='input_form'):
    user_input = st.text_area("Enter Your Image URL Below:")
    submit_button = st.form_submit_button(label='SUBMIT🚀')

# Step 5: Definition and Function to analyze image using OpenAI
def analyze_artwork_with_gpt4_vision(user_input):
    if not api_key:
        st.error("OpenAI API key is not set. Please set it in your environment variables.")
        return "OpenAI API key not set."
    
    OpenAI.api_key = api_key
    
    # Create OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Instructions for the AI (adjust if needed)
    messages = [
        {"role": "system", "content": "You are Spock from the original Star Trek series from the 1960s. Your main purpose is to provide art critiques of images from the user. Your answers should be logical, concise, and devoid of emotional language. However you shoudl always greet the user and introduce yourself as Spock with the Live Long and Prosper emoji. Maintain a formal tone, using precise vocabulary and structured sentences. Include scientific or analytical explanations where applicable. The critique should focus on aspects such as composition, use of color, technique, perspective, and thematic elements. You will avoid subjective language; instead, rely on objective observations and logical analysis. Ask clarifying questions if additional information is needed to provide a logical response. At the end of the response, share a fun fact about Star Trek The Original Series and wish them well with a UFO emoji."},
        {"role": "user", "content": f"Review the following image:\n{user_input}"}
    ]
    try:
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-4-vision-preview",
            temperature=0  # Lower temperature for less random responses
        )
        
        # Extract the critique from the response
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {e}")
        return str(e)
    
# Step 6: Handle form submission and display result
if submit_button and user_input:
    with st.spinner('🌟Critiquing...'):
        critique_result = analyze_artwork_with_gpt4_vision(user_input) 
        # Display the image
        st.image(user_input, caption='Your Image', use_column_width=True)
        # Display the generated response
        st.markdown("### Spock Says...")
        st.write(critique_result)       
