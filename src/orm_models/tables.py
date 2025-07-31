import datetime
import uuid

from sqlalchemy import TIMESTAMP, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.orm_models.base_class import Base


class Users(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    token: Mapped[str] = mapped_column(
        String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc)
    )

    records: Mapped["AudioRecord"] = relationship("AudioRecord", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"


class AudioRecord(Base):

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    original_filename: Mapped[str] = mapped_column(String(100), nullable=False)
    mp3_filename: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc)
    )

    user: Mapped["Users"] = relationship("Users", back_populates="records")
