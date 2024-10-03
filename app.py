from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional

class Meme(BaseModel):
    comment: str = Field(..., max_length=100)
    photo: str = Field(...)
    visibility: Optional[bool] = Field(default=False)

class ChangeVisibility(BaseModel):
    meme_id: UUID
    visibility: bool

