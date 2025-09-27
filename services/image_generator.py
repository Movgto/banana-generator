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

prompt = (
    '''        
        An image of a survival-horror game located on a typical mexican town.        
        Kizin, one of the deities of the mayan underworld has sent horrible paranormal creatures
        sobrenaturales con aspecto cadaverico, llamados los Kimen, la descripción es la siguiente:
        with cadaveric aspect, they're called Kimen, their description is the following:

        La palabra "kimen" significa "muerto" o "cadáver" en la lengua maya yucateca, y los kimen son criaturas de Xibalbá(el inframundo maya)
        creadas para erradicar a la humanidad. A diferencia de los zombis modernos, los kimen se descomponen y la enfermedad se propaga al simple contacto,
        contaminando todo a su paso.

        The word "kimen" means "dead" or "corpse" in the yucateca maya tongue, and the kimen are creatures of Xibalba, the mayan underworld
        created to extermine humanity. In contrast to modern zombies, the kimen are constantly in state of decomposition
        and the sickness propagates only with their touch, contaminating everything in their path.
        
        A kid is visible, the player, it has just went out of his house and finds the streets infested of kimen.

        The game is in a 3rd person view, and the graphics are PS1 style.      
    '''
)

def generate_image(prompt: str):    

    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=[prompt],
    )

    print(response)

    if response and response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data and part.inline_data.data:
                print('Generando imagen...')            
                image: Image.Image = Image.open(BytesIO(part.inline_data.data))
                return image

        return None          