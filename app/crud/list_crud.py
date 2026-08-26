"""TODOリストのDB操作."""

from app.dependencies import DbSession
from app.models.list_model import ListModel


def get_todo_list(db: DbSession, todo_list_id: int):
    """TODOリストを1件取得する."""
    return db.query(ListModel).filter(ListModel.id == todo_list_id).first()
