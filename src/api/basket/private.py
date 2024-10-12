from fastapi import status
from .router import router
from uuid import uuid4
from src.schemas import meme
from random import randint


@router.get('/private/random', status_code=status.HTTP_200_OK)
async def get_random_public_meme() -> meme.Meme:
    # Logic

    return meme.Meme(
        id=uuid4(),
        user_id=1,
        comment='Random private meme',
        photo='https://example.com/public_meme.jpg',
        public=True,
        likes=100,
        dislikes=50,
    )


@router.get('/private/memes', status_code=status.HTTP_200_OK)
async def get_random_public_meme() -> list[meme.Meme]:
    # Logic

    return [meme.Meme(
        id=uuid4(),
        user_id=1,
        comment='Random private meme',
        photo='https://example.com/public_meme.jpg',
        public=randint(0, 1),
        likes=randint(1, 100),
        dislikes=randint(0, 100),
    ) for _ in range(10)]