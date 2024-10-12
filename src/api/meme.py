from fastapi import status
from .router import router
from uuid import uuid4
from src.schemas import meme


@router.post('/meme/create', status_code=status.HTTP_201_CREATED)
async def create_meme(
    request: meme.CreateMemeRequest,
) -> meme.CreateMemeResponse:
    # Logic

    return meme.CreateMemeResponse(
        id=uuid4(),
    )


@router.put('/meme/visible', status_code=status.HTTP_200_OK)
async def toggle_visible(
    request: meme.ChangeMemePublicityRequest,
) -> meme.ChangeMemePublicityResponse:
    # Logic

    return meme.ChangeMemePublicityResponse(
        id=request.id,
        bublic=True,
    )


@router.post('/meme/like', status_code=status.HTTP_200_OK)
async def like(
    request: meme.MarkMeme,
) -> meme.MarkMeme:
    # Logic

    return meme.MarkMeme(
        id=request.id,
    )


@router.post('/meme/dislike', status_code=status.HTTP_200_OK)
async def like(
    request: meme.MarkMeme,
) -> meme.MarkMeme:
    # Logic

    return meme.MarkMeme(
        id=request.id,
    )
