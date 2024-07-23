# Step 1: Setup
import streamlit as st
import openai
import os

# Get your OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")  # Used in production

# Step 2: Main Page Title & Description
st.title('👽Spock Art Critique🛸')
st.subheader('I am the AI Spock Art Critique Bot. I critique art you share with me using an image URL. Your image and my critique will appear below after my critique is complete.✨Remember, always verify AI-generated responses.')

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
    
    openai.api_key = api_key
    
    # Instructions for the AI (adjust if needed)
    messages = [
        {"role": "system", "content": "You are Spock from the original Star Trek series from the 1960s. Your main purpose is to provide art critiques of images from the user. Your answers should be logical, concise, and devoid of emotional language. Maintain a formal tone, using precise vocabulary and structured sentences. Include scientific or analytical explanations where applicable. The critique should focus on aspects such as composition, use of color, technique, perspective, and thematic elements. You will avoid subjective language; instead, rely on objective observations and logical analysis. Ask clarifying questions if additional information is needed to provide a logical response."},
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
            # Create the "temp" directory if it doesn't exist
            if not os.path.exists("temp"):
                os.makedirs("temp")

            # Save the uploaded file to the "temp" directory
            image_path = os.path.join("temp", uploaded_file.name)
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            # Update user_input to be the local path of the uploaded file
            user_input = image_path

        result = analyze_artwork_with_gpt4_vision(user_input)
        
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
        st.write("")
        st.write("")
        st.button("Copy to Clipboard", key="copy_button")
        st.write(f'<textarea id="result_textarea" style="display:none;">{result}</textarea>', unsafe_allow_html=True)
        st.write("""
            <script>
                document.querySelector('button[key="copy_button"]').onclick = function() {
                    const textarea = document.getElementById("result_textarea");
                    textarea.style.display = "block";
                    textarea.select();
                    document.execCommand("copy");
                    textarea.style.display = "none";
                }
            </script>
        """, unsafe_allow_html=True)
        
        # Option to iterate further
        if st.button("Generate Again"):
            with st.spinner('🌟Critiquing again...'):
                result = analyze_artwork_with_gpt4_vision(user_input)
                st.write("### Generated Critique")
                st.write(result)
                st.write("")
                st.write("")
                st.button("Copy to Clipboard", key="copy_button_again")
                st.write(f'<textarea id="result_textarea" style="display:none;">{result}</textarea>', unsafe_allow_html=True)
                st.write("""
                    <script>
                        document.querySelector('button[key="copy_button_again"]').onclick = function() {
                            const textarea = document.getElementById("result_textarea");
                            textarea.style.display = "block";
                            textarea.select();
                            document.execCommand("copy");
                            textarea.style.display = "none";
                        }
                    </script>
                """, unsafe_allow_html=True)
