import os
from dotenv import load_dotenv
from google import genai
from io import BytesIO
from PIL import Image, ImageFile
from typing import Optional, Any
from services.interfaces import ChatMessage
from datetime import datetime

from services.image_generator_adapters import ImageGeneratorAdapter, GeminiGenerator
load_dotenv()

print(f'API KEY: {os.environ.get('API_KEY')}')

client = genai.Client(
    api_key= os.environ.get('API_KEY')
)

def generate_image(conversation: list[ChatMessage], image: Optional[ImageFile.ImageFile] = None, image_generator_adapter: ImageGeneratorAdapter = GeminiGenerator()):    
    messages = tuple(f'{msg.role}: {msg.content}' for msg in conversation if type(msg.content) == str)

    prompt =  '\n'.join(messages)
    print('Prompt:')
    print(prompt)
    
    return image_generator_adapter.generate(prompt, image)