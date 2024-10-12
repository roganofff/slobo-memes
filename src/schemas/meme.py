"""JSON models for work with memes."""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class IDMixin:
    id: UUID = Field(...)


class CreateMemeRequest(BaseModel):
    """JSON request model for create meme."""

    comment: str = Field(..., max_length=100, description='Comment for meme.')
    photo: str = Field(..., description='Meme image.')
    public: Optional[bool] = Field(
        default=False,
        description='Are all users can see this meme.',
    )


class CreateMemeResponse(IDMixin, BaseModel):
    """JSON response model for create meme."""


class ChangeMemePublicityRequest(IDMixin, BaseModel):
    """JSON request model for toggle meme visibility."""


class ChangeMemePublicityResponse(IDMixin, BaseModel):
    """JSON response model for toggle meme visibility."""

    public: bool = Field(..., descriprion='Meme visibility after toggle.')


class MarkMeme(IDMixin, BaseModel):
    """JSON request/response model for like/dislike meme."""


class Meme(IDMixin, BaseModel):
    """JSON model for meme."""

    user_id: int = Field(..., description='Who add meme.')
    comment: str = Field(..., description='Comment for meme.')
    photo: str = Field(..., description='Meme image.')
    public: bool = Field(..., description='Are all users can see this meme.')
    likes: int = Field(default=0, description='Number of likes.')
    dislikes: int = Field(default=0, description='Number of dislikes.')
