"""TODOリストのDB操作."""

from sqlalchemy.orm import Session

from app.models.list_model import ListModel


def get_todo_list(db: Session, todo_list_id: int) -> ListModel | None:
    """TODOリストを1件取得する."""
    return db.query(ListModel).filter(ListModel.id == todo_list_id).first()
