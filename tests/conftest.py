import pytest
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app.models import item_model, list_model


@pytest.fixture(autouse=False)
def db_session():
    db = SessionLocal()
    try:
        _reset_records(db)
        yield db
    finally:
        _reset_records(db)
        db.close()


def refresh_session(db: Session) -> None:
    """API呼び出し後にテスト用DBセッションの状態をリセットする."""
    db.rollback()
    db.expire_all()


def _reset_records(db: Session) -> None:
    """テーブルのレコードをリセット."""
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    is_deleted = False

    if ("todo_lists" in table_names):
        db.query(list_model.ListModel).delete()
        is_deleted = True
    if ("todo_items" in table_names):
        db.query(item_model.ItemModel).delete()
        is_deleted = True

    if is_deleted:
        db.commit()
