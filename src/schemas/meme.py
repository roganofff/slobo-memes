"""JSON models for work with memes."""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class CreateMemeRequest(BaseModel):
    """JSON request model for creating meme."""

    comment: str = Field(..., max_length=100)
    photo: str = Field(...)
    visibility: Optional[bool] = Field(default=False)


class CreateMemeResponse(BaseModel):
    """JSON response model for creating meme."""

    id: UUID = Field(...)


class ChangeMemeVisibilityRequest(BaseModel):
    """JSON request model for toggling meme visibility."""

    id: UUID = Field(...)


class ChangeMemeVisibilityResponse(BaseModel):
    """JSON response model for toggling meme visibility."""

    id: UUID = Field(...)
    visibility: bool = Field(...)
