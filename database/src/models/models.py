import uuid
from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    Text,
    String,
    Index,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models.meta import Base


class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)


class Meme(UUIDMixin, Base):
    __tablename__ = 'memes'
    
    creator_id: Mapped[int] = mapped_column(BigInteger, index=True)
    image_url: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(String(250), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    
    ratings: Mapped[list['Rating']] = relationship(cascade='all, delete-orphan')
    saved_by: Mapped[list['Saved']] = relationship(cascade='all, delete-orphan')


class Rating(UUIDMixin, Base):
    __tablename__ = 'ratings'
    
    meme_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('memes.id', ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(BigInteger)
    is_like: Mapped[bool] = mapped_column(Boolean)
    
    __table_args__ = (
        UniqueConstraint('meme_id', 'user_id', name='uq_ratings_meme_user'),
        Index('ix_ratings_meme_id_is_like', 'meme_id', 'is_like'),
        Index('ix_ratings_meme_id_user_id', 'meme_id', 'user_id'),
    )


class Saved(UUIDMixin, Base):
    __tablename__ = 'saved'
    
    meme_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('memes.id', ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)

    meme: Mapped['Meme'] = relationship(back_populates='saved_by')

    __table_args__ = (
        UniqueConstraint('meme_id', 'user_id', name='uq_saved_meme_user'),
        Index('ix_saved_meme_id_user_id', 'meme_id', 'user_id'),
    )

