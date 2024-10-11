from fastapi import status, HTTPException
from .router import router
from uuid import uuid4
from src.schemas import meme

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_meme(
    request: meme.CreateMemeRequest,
) -> meme.CreateMemeResponse:
    # Logic

    return meme.CreateMemeResponse(
        id=uuid4(),
    )

@router.put('/visible', status_code=status.HTTP_200_OK)
async def create_meme(
    request: meme.ChangeMemeVisibilityRequest,
) -> meme.CreateMemeResponse:
    # Logic

    return meme.ChangeMemeVisibilityRequest(
        id=request.id,
        visibility=True,
    )
