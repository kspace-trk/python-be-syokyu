from datetime import datetime
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import DateTime, Integer, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.item_model import ItemModel


class ListModel(Base):
    """TODOリストモデル."""

    __tablename__ = "todo_lists"
    __table_args__: ClassVar[dict[str]] = {
        "comment": "TODOリストテーブル",
    }

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column("title", String(50), nullable=False)
    description: Mapped[str | None] = mapped_column("description", String(200))
    created_at: Mapped[datetime] = mapped_column("created_at", DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at",
        DateTime,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
    items: Mapped[list["ItemModel"]] = relationship(back_populates="todo_list")
