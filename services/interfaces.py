from typing import Literal, Optional, NamedTuple
from PIL import ImageFile

class ChatMessage(NamedTuple):
    role: Literal['user','assistant']
    content: Optional[str] = None
    image: Optional[ImageFile.ImageFile] = None