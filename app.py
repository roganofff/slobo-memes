"""Initialize & added API method's for bot."""
from typing import Optional
from uuid import UUID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class Meme(BaseModel):
    """Model for API methods."""

    comment: str = Field(..., max_length=100)
    photo: str = Field(...)
    visibility: Optional[bool] = Field(default=False)


class ChangeVisibility(BaseModel):
    """Model for API methods."""

    meme_id: UUID
    visibility: bool
