# Step 1: Setup
import streamlit as st
from openai import OpenAI
import os
import streamlit_copy_to_clipboard as stc

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
    user_input = st.text_area("Enter Your Image URL Here")
    uploaded_file = st.file_uploader("Or upload an image file", type=["jpg", "jpeg", "png"])
    submit_button = st.form_submit_button(label='🚀Submit🚀!')

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
if submit_button and (user_input or uploaded_file):
    with st.spinner('🌟Critiquing...'):
        # If a file is uploaded, use that file for the critique
        if uploaded_file:
            # Save the uploaded file to a temporary location
            image_path = os.path.join("temp", uploaded_file.name)
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            # Update user_input to be the local path of the uploaded file
            user_input = image_path

        result = critique_art(user_input)
        
        # Show the image URL or uploaded image on the main page
        st.write("### Entered Image URL or Uploaded Image")
        if uploaded_file:
            st.image(user_input, caption='Uploaded Image', use_column_width=True)
        else:
            st.write(user_input)
            st.image(user_input, caption='Entered Image', use_column_width=True)
        
        # Display the generated response
        st.write("### Generated Critique")
        st.write(result)
        
        # Copy to clipboard button
        stc.copy_to_clipboard(result)
        
        # Option to iterate further
        if st.button("Generate Again"):
            with st.spinner('🌟Critiquing again...'):
                result = critique_art(user_input)
                st.write("### Generated Critique")
                st.write(result)
                stc.copy_to_clipboard(result)   
