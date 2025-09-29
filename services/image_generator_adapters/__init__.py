import boto3
import random
import json
import os
from typing import Protocol
from google import genai
from io import BytesIO
from PIL import Image, ImageFile
from typing import Optional, Any
from datetime import datetime
import dotenv
import base64

dotenv.load_dotenv()


class ImageGeneratorAdapter(Protocol):
    def generate(self, prompt: str, image: Optional[ImageFile.ImageFile]
                 = None) -> tuple[str | None, ImageFile.ImageFile | None]: ...


class GeminiGenerator:
    client = genai.Client(
        api_key=os.environ.get('API_KEY')
    )

    def generate(self, prompt: str, image: Optional[ImageFile.ImageFile] = None) -> tuple[str | None, ImageFile.ImageFile | None]:

        contents: list[Any] = [prompt]

        if image:
            contents.append(image.convert())
        response = GeminiGenerator.client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=contents
        )

        print(response)
        text = None
        image = None
        if response and response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:

                if part.text is not None:
                    print(part.text)
                    text = part.text
                elif part.inline_data and part.inline_data.data:
                    print('Generando imagen...')
                    image = Image.open(BytesIO(part.inline_data.data))

                    path_to_images = os.path.join(os.path.dirname(
                        os.path.dirname(__file__)), 'images')
                    date_str = datetime.strftime(
                        datetime.today(), '%d_%m_%YT%H%M%S')
                    os.makedirs(path_to_images, exist_ok=True)
                    with open(os.path.join(path_to_images, f'image_{date_str}.png'), 'wb') as file:
                        image.save(file, 'png')

        return text, image


class AmazonGenerator:
    client = boto3.client(
        "bedrock-runtime",
        region_name="us-east-1",
    )

    def generate(self, prompt: str, image: Optional[ImageFile.ImageFile] = None) -> tuple[str | None, ImageFile.ImageFile | None]:
        text, image = None, None

        # Set the model ID.
        model_id = "amazon.nova-canvas-v1:0"                

        # Generate a random seed between 0 and 858,993,459
        seed = random.randint(0, 858993460)

        # Format the request payload using the model's native structure.
        native_request = {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {"text": prompt},
            "imageGenerationConfig": {
                "seed": seed,
                "quality": "standard",
                "height": 512,
                "width": 512,
                "numberOfImages": 1,
            },
        }

        # Convert the native request to JSON.
        request = json.dumps(native_request)

        # Invoke the model with the request.
        response = AmazonGenerator.client.invoke_model(
            modelId=model_id, body=request)

        # Decode the response body.
        model_response = json.loads(response["body"].read())

        # Extract the image data.
        base64_image_data = model_response["images"][0]
        
        image_data = base64.b64decode(base64_image_data)
        
        print(f'Image data: {image_data}')

        if base64_image_data:
            path_to_images = os.path.join(os.path.dirname(
                os.path.dirname(__file__)), 'images')
            date_str = datetime.strftime(
                datetime.today(), '%d_%m_%YT%H%M%S')
            os.makedirs(path_to_images, exist_ok=True)
                        
            image = Image.open(BytesIO(image_data))
            with open(os.path.join(path_to_images, f'image_{date_str}.png'), 'wb') as file:
                image.save(file, format='png')

        return text, image
