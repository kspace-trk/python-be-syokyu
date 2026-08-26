"""TODO項目のDB操作."""

from sqlalchemy.orm import Session

from app.const import TodoItemStatusCode
from app.models.item_model import ItemModel
from app.schemas.item_schema import NewTodoItem, UpdateTodoItem


def get_todo_item(db: Session, todo_list_id: int, todo_item_id: int) -> ItemModel | None:
    """TODO項目を1件取得する."""
    # todo_list_idとtodo_item_idの両方で絞り込み、別リストの項目を取得しないようにする
    return db.query(ItemModel).filter(ItemModel.id == todo_item_id, ItemModel.todo_list_id == todo_list_id).first()


def create_todo_item(db: Session, todo_list_id: int, new_todo_item: NewTodoItem) -> ItemModel:
    """TODO項目を1件登録する."""
    # 親リストのidはパスパラメータから取得し、ボディの値と合わせてインスタンスを生成する
    db_item = ItemModel(
        todo_list_id=todo_list_id,
        title=new_todo_item.title,
        description=new_todo_item.description,
        due_at=new_todo_item.due_at,
        # ステータスの初期値は「未完了」。.value で列挙型から実際の数値を取り出す
        status_code=TodoItemStatusCode.NOT_COMPLETED.value,
    )
    # addしてcommitすることで、DBに保存
    db.add(db_item)
    db.commit()
    # DB保存によって採番されたidやcreated_atをdb_itemオブジェクトに反映
    db.refresh(db_item)
    return db_item


def update_todo_item(
    db: Session,
    todo_list_id: int,
    todo_item_id: int,
    update_todo_item: UpdateTodoItem,
) -> ItemModel | None:
    """TODO項目を1件更新する."""
    db_item = get_todo_item(db, todo_list_id, todo_item_id)
    if db_item is None:
        return None
    # 任意項目のため、値が渡された（None でない）ときだけ書き換える
    if update_todo_item.title is not None:
        db_item.title = update_todo_item.title
    if update_todo_item.description is not None:
        db_item.description = update_todo_item.description
    if update_todo_item.due_at is not None:
        db_item.due_at = update_todo_item.due_at
    # completeはFalseも有効な値なので、if文ではなくNoneかどうかで判定する
    if update_todo_item.complete is not None:
        # 真偽値のcompleteを、DBに保存するstatus_codeへ変換する
        if update_todo_item.complete:
            db_item.status_code = TodoItemStatusCode.COMPLETED.value
        else:
            db_item.status_code = TodoItemStatusCode.NOT_COMPLETED.value
    # 書き換えた属性をDBに反映
    db.commit()
    # 更新後のupdated_atなどをdb_itemオブジェクトに反映
    db.refresh(db_item)
    return db_item


def delete_todo_item(db: Session, todo_list_id: int, todo_item_id: int) -> bool:
    """TODO項目を1件削除し、削除できたか否かを返す."""
    db_item = get_todo_item(db, todo_list_id, todo_item_id)
    if db_item is None:
        return False
    # レコードを削除してDBに反映
    db.delete(db_item)
    db.commit()
    return True
