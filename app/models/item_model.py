from datetime import datetime
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import DateTime, ForeignKey, Integer, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.list_model import ListModel


class ItemModel(Base):
    """アイテムモデル."""
    __tablename__ = "todo_items"
    __table_args__: ClassVar[dict[str]] = {
        "comment": "アイテムテーブル",
    }

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    todo_list_id: Mapped[int] = mapped_column("todo_list_id", Integer, ForeignKey("todo_lists.id"), nullable=False)
    title: Mapped[str] = mapped_column("title", String(50), nullable=False)
    description: Mapped[str | None] = mapped_column("description", String(200))
    status_code: Mapped[int | None] = mapped_column("status_code", Integer)
    due_at: Mapped[datetime | None] = mapped_column("due_at", DateTime)
    created_at: Mapped[datetime] = mapped_column("created_at", DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at",
        DateTime,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
    todo_list: Mapped["ListModel"] = relationship(back_populates="items")
