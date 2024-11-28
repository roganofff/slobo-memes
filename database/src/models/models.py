from sqlalchemy import UUID, BigInteger, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.models.meta import Base
import uuid


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
