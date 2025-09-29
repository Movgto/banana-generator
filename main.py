import streamlit as st
from services.image_generator import generate_image
from typing import NamedTuple, Literal, Optional
from PIL import ImageFile, Image
from io import BytesIO
from services.interfaces import ChatMessage
from services.image_generator_adapters import AmazonGenerator

st.title("Image Generator")
edit_last_image = st.checkbox('Edit last image?')
uploaded_image = st.file_uploader('Upload Image')

prompt = st.chat_input("Enter your image prompt...")


if 'conversation' not in st.session_state:
    st.session_state.conversation = []

if 'last_image' not in st.session_state:
    st.session_state.last_image = None

if prompt:    
    st.session_state.conversation.append(ChatMessage(role='user', content=prompt))

    print(f'Uploaded file type: {type(uploaded_image)}')

    results = None
    with st.spinner(f"Generating image...", show_time=True):
        uploaded_image_open = None
        if uploaded_image:        
            uploaded_image_open = Image.open(uploaded_image)
        
        results = generate_image(st.session_state.conversation, st.session_state.last_image if edit_last_image else (uploaded_image_open if uploaded_image else None))
    
    text, image = results

    st.session_state.last_image = image

    st.session_state.conversation.append(ChatMessage(role='assistant', content=text, image=image))

for msg in st.session_state.conversation:
    match msg.role:
        case 'user':
            st.chat_message('user').write(msg.content)
        case 'assistant':
            with st.chat_message('assistant'):
                if msg.content:
                    st.write(msg.content)
                if msg.image:
                    print('Mostrando imagen...')
                    st.image(msg.image.convert(), caption='Generated Image')
