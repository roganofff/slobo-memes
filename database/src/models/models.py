from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import UUID, BigInteger, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.models.meta import Base
import uuid
from typing import Self

from src.storage.database import get_db
from src.utils.inject_database import inject, Provide


class Meme(Base):
    __tablename__ = 'memes'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        index=True,
    )
    text: Mapped[str] = mapped_column(
        String(250),
        nullable=True,
    )
    image_url: Mapped[str] = mapped_column(
        Text,
    )
    public: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    @staticmethod
    @inject
    async def add(
        user_id: int,
        text: str,
        image_url: str,
        session: AsyncSession = Provide(get_db)
    ) -> 'Meme':
        meme = Meme(
            user_id=user_id,
            text=text,
            image_url=image_url,
        )
        session.add(meme)
        await session.commit()
        return meme
