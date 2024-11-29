from typing import TypedDict

class Meme(TypedDict):
    id: str
    user_id: int
    text: str
    image_url: str
    public: bool


class AddMeme(TypedDict):
    user_id: int
    text: str
    image_url: str