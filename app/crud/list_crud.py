"""TODOリストのDB操作."""

from sqlalchemy.orm import Session

from app.models.list_model import ListModel
from app.schemas.list_schema import NewTodoList, UpdateTodoList


def get_todo_list(db: Session, todo_list_id: int) -> ListModel | None:
    """TODOリストを1件取得する."""
    return db.query(ListModel).filter(ListModel.id == todo_list_id).first()


def create_todo_list(db: Session, new_todo_list: NewTodoList) -> ListModel:
    """TODOリストを1件登録する."""
    # ListModelクラスのインスタンスを生成する
    db_item = ListModel(title=new_todo_list.title, description=new_todo_list.description)
    # addしてcommitすることで、DBに保存
    db.add(db_item)
    db.commit()
    # DB保存によって採番されたidやcreated_atをdb_itemオブジェクトに反映
    db.refresh(db_item)
    return db_item


def update_todo_list(db: Session, todo_list_id: int, update_todo_list: UpdateTodoList) -> ListModel | None:
    """TODOリストを1件更新する."""
    db_item = get_todo_list(db, todo_list_id)
    if db_item is None:
        return None
    # 任意項目のため、値が渡された（None でない）ときだけ書き換える
    if update_todo_list.title is not None:
        db_item.title = update_todo_list.title
    if update_todo_list.description is not None:
        db_item.description = update_todo_list.description
    # 書き換えた属性をDBに反映
    db.commit()
    # 更新後のupdated_atなどをdb_itemオブジェクトに反映
    db.refresh(db_item)
    return db_item


def delete_todo_list(db: Session, todo_list_id: int) -> bool:
    """TODOリストを1件削除し、削除できたか否かを返す."""
    db_item = get_todo_list(db, todo_list_id)
    if db_item is None:
        return False
    # レコードを削除してDBに反映
    db.delete(db_item)
    db.commit()
    return True
