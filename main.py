import streamlit as st
from services.image_generator import generate_image

st.title("Image Generator")

prompt = st.text_area("Enter your image prompt:")

if st.button("Generate Image"):
    if prompt:
        
        results = None
        with st.spinner(f"Generating image...", show_time=True):
                        
            results = generate_image(prompt)
        
        text, image = results
        
        
        st.success(text or 'Done!')      
        if image:            
            st.image(image.convert(), caption="Generated Image")
        else:
            st.warning('The Image could not be generated.')
    else:
        st.warning("Please enter a prompt to generate an image.")
