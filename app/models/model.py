from typing import List,Optional
from sqlalchemy.orm import Mapped
# Для полей таблицы.
from sqlalchemy import ForeignKey,Text,DateTime,String
from sqlalchemy.orm import mapped_column
# Чтобы связывать модели между собой
from sqlalchemy.orm import relationship 
# Базовый класс для всех моделей.
from sqlalchemy.orm import DeclarativeBase
# Чтобы автоматически проставлять даты создания и обновления.
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

# TODO: Добавить модель для тэгов и связь многие-ко-многим между заметками и тэгами.
# TODO: когда добавишь больше моделей, создай отдельный файл base.py с Base и __all_models_imports__, чтобы Alembic автоматически подтягивал все таблицы при autogenerate.

class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True) 
    username:Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False
        )
    hashed_email:Mapped[str] = mapped_column(
        String(64),
        index=True,
        unique=True,
        nullable=False
        )
    hashed_password:Mapped[str] = mapped_column(
        String(255),
        nullable=False
        )
    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc),
        nullable=False
    )
    notes:Mapped[List["Note"]] = relationship(
        back_populates="owner",
        cascade="all, delete, delete-orphan",
        passive_deletes=True
        )
    
    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r})"
    
class Note(Base):
    __tablename__ = "notes"
    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(
        String(200),
        nullable=False
        )
    content:Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
        )
    owner_id:Mapped[int] = mapped_column(
        ForeignKey("users.id",ondelete="CASCADE"),
        nullable=False,
        index=True
        )
    tags:Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        )
    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc),
        nullable=False
    )
    updated_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc),
        onupdate=lambda:datetime.now(timezone.utc),
        nullable=False
    )
    owner:Mapped[User] = relationship(back_populates="notes")
    
    def __repr__(self)-> str:
        return f"Note(id={self.id!r}, title={self.title[:15]!r}, owner_id={self.owner_id!r})" 
        