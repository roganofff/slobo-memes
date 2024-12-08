from typing import Optional, TypedDict


class Meme(TypedDict):
    id: str
    creator_id: int
    description: str
    image_url: str
    is_public: bool
    likes: int
    dislikes: int
    user_rating: Optional[bool]
    is_saved: bool
    pagination: tuple[str | None, str | None]


class AddMeme(TypedDict):
    creator_id: int
    description: str
    image_url: str


class RandomMeme(TypedDict):
    user_id: int
    public_only: bool


class RateMeme(TypedDict):
    meme_id: str
    user_id: int
    new_rating: bool


class RemoveRating(TypedDict):
    meme_id: str
    user_id: int


class MemeSaves(TypedDict):
    meme_id: str
    user_id: int


class ChangeVisibility(TypedDict):
    meme_id: str
    user_id: int
    new_visibility: bool


class FirstSavedMeme(TypedDict):
    user_id: int


class SavedMeme(TypedDict):
    user_id: int
    saved_id: str
