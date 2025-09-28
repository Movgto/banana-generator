import os
from dotenv import load_dotenv
from google import genai
from io import BytesIO
from PIL import Image

load_dotenv()

print(f'API KEY: {os.environ.get('API_KEY')}')

client = genai.Client(
    api_key= os.environ.get('API_KEY')
)

def generate_image(prompt: str):    

    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=[prompt],
    )

    print(response)
    text = None
    image = None
    if response and response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            results = set()
            if part.text is not None:
                print(part.text)
                text = part.text
            elif part.inline_data and part.inline_data.data:
                print('Generando imagen...')            
                image = Image.open(BytesIO(part.inline_data.data))
                                        
    return (text, image)