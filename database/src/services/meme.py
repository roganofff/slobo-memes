import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import select, func

from src.models import Meme, Rating, Saved
from src.schema.meme import Meme as MemeDict
from src.utils.inject_database import Provide, inject
from src.storage.database import get_db


class MemeService:
    @staticmethod
    @inject
    async def __get_mark_count(
        meme: Meme,
        mark: bool,
        session: AsyncSession = Provide(get_db),
    ) -> int:
        statement = select(func.count()).where(
            Rating.meme_id == meme.id,
            Rating.is_like == mark,
        ).select_from(Rating)
        return (await session.execute(statement)).scalar()

    @staticmethod
    @inject
    async def build_meme_response(
        meme: Meme,
        user_id: int,
        likes: Optional[int] = None,
        dislikes: Optional[int] = None,
        user_rating: Optional[bool] = None,
        is_saved: Optional[bool] = None,
        session: AsyncSession = Provide(get_db),
    ) -> MemeDict:
        if likes is None:
            likes = await MemeService.__get_mark_count(meme, True)
        if dislikes is None:
            dislikes = await MemeService.__get_mark_count(meme, False)
        if user_rating is None:
            user_rating = await session.execute(
                select(Rating).where(Rating.meme_id == meme.id, Rating.user_id == user_id)
            )
            user_rating: Rating = user_rating.scalars().first()
            user_rating = user_rating.is_like if user_rating is not None else None
        if is_saved is None:
            is_saved = await session.execute(
                select(Saved).where(Saved.meme_id == meme.id, Saved.user_id == user_id)
            )
            is_saved = is_saved.scalars().first() is not None
        return MemeDict(
            id=str(meme.id),
            creator_id=meme.creator_id,
            description=meme.description,
            image_url=meme.image_url,
            is_public=meme.is_public,
            likes=likes,
            dislikes=dislikes,
            user_rating=user_rating,
            is_saved=is_saved,
        )

    @staticmethod
    @inject
    async def add_meme(
        creator_id: int,
        description: str,
        image_url: str,
        session: AsyncSession = Provide(get_db),
    ) -> MemeDict:
        new_meme = Meme(
            creator_id=creator_id,
            description=description,
            image_url=image_url,
        )
        session.add(new_meme)
        await session.flush()
        new_save = Saved(
            meme_id=new_meme.id,
            user_id=creator_id,
        )
        session.add(new_save)
        await session.commit()
        return await MemeService.build_meme_response(
            new_meme,
            creator_id,
            likes=0,
            dislikes=0,
            user_rating=None,
            is_saved=True,
        )

    @staticmethod
    @inject
    async def get_random_meme(
        user_id: int,
        public_only: bool,
        session: AsyncSession = Provide(get_db),
    ) -> Optional[MemeDict]:
        if public_only:
            statement = select(Meme).where(Meme.is_public == True)
        else:
            statement = select(Meme).join(
                Saved,
                Saved.meme_id == Meme.id,
            ).where(Saved.user_id == user_id)
        meme = await session.execute(statement.order_by(func.random()))
        meme = meme.scalars().first()
        if not meme:
            return None
        return await MemeService.build_meme_response(meme, user_id)

    @staticmethod
    @inject
    async def rate_meme(
        meme_id: uuid.UUID,
        user_id: int,
        new_rating: bool,
        session: AsyncSession = Provide(get_db),
    ) -> Optional[MemeDict]:
        meme = await session.get(Meme, meme_id)
        if not meme:
            return None
        statement = select(Rating).where(Rating.meme_id == meme_id, Rating.user_id == user_id)
        rating = await session.execute(statement)
        rating = rating.scalars().first()
        if rating:
            rating.is_like = new_rating
        else:
            rating = Rating(meme_id=meme_id, user_id=user_id, is_like=new_rating)
            session.add(rating)
        await session.commit()
        return await MemeService.build_meme_response(
            meme,
            user_id,
            user_rating=rating.is_like
        )

    @staticmethod
    @inject
    async def remove_rating(
        meme_id: uuid.UUID,
        user_id: int,
        session: AsyncSession = Provide(get_db),
    ) -> Optional[MemeDict]:
        meme = await session.get(Meme, meme_id)
        if not meme:
            return None
        statement = select(Rating).where(Rating.meme_id == meme_id, Rating.user_id == user_id)
        rating = await session.execute(statement)
        rating = rating.scalars().first()
        if rating:
            await session.delete(rating)
            await session.commit()
        return await MemeService.build_meme_response(meme, user_id)

    @staticmethod
    @inject
    async def add_to_saved(
        meme_id: uuid.UUID,
        user_id: int,
        session: AsyncSession = Provide(get_db),
    ) -> MemeDict:
        try:
            saved = Saved(meme_id=meme_id, user_id=user_id)
            session.add(saved)
            await session.commit()
        except IntegrityError:
            await session.rollback()
        meme = await session.get(Meme, meme_id)
        return await MemeService.build_meme_response(session, meme, user_id)

    @staticmethod
    @inject
    async def remove_from_saved(
        meme_id: uuid.UUID,
        user_id: int,
        session: AsyncSession = Provide(get_db),
    ) -> MemeDict:
        statement = select(Saved).where(Saved.meme_id == meme_id, Saved.user_id == user_id)
        saved = await session.execute(statement)
        saved = saved.scalars().first()
        if saved:
            await session.delete(saved)
            await session.commit()
        meme = await session.get(Meme, meme_id)
        return await MemeService.build_meme_response(session, meme, user_id)

    @staticmethod
    @inject
    async def change_visibility(
        meme_id: uuid.UUID,
        user_id: int,
        new_visibility: bool,
        session: AsyncSession = Provide(get_db),
    ) -> Optional[MemeDict]:
        statement = select(Meme).where(Meme.id == meme_id, Meme.creator_id == user_id)
        meme = await session.execute(statement)
        meme = meme.scalars().first()
        if not meme:
            return None
        meme.is_public = new_visibility
        await session.commit()
        return await MemeService.build_meme_response(session, meme, user_id)

    @staticmethod
    @inject
    async def delete_meme(
        meme_id: uuid.UUID,
        user_id: int,
        session: AsyncSession = Provide(get_db),
    ) -> bool:
        statement = select(Meme).where(Meme.id == meme_id, Meme.creator_id == user_id)
        meme = await session.execute(statement)
        meme = meme.scalars().first()
        if not meme:
            return False
        await session.delete(meme)
        await session.commit()
        return True
