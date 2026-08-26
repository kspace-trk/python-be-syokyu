"""TODOリストのAPI."""

from fastapi import APIRouter

from app.dependencies import DbSession
from app.models.list_model import ListModel
from app.schemas.list_schema import NewTodoList, ResponseTodoList, UpdateTodoList
from app.crud import list_crud

# prefixでパスの共通部分を、tagsでSwagger UI上のグループをまとめて指定する
router = APIRouter(
    prefix="/lists",
    tags=["Todoリスト"],
)


# prefixが付くため、デコレータには/lists以降だけを書く
@router.get("/{todo_list_id}", response_model=ResponseTodoList)
def get_todo_list(todo_list_id: int, db: DbSession):
    return list_crud.get_todo_list(db, todo_list_id)


@router.post("/", response_model=ResponseTodoList)
def post_todo_list(new_todo_list: NewTodoList, db: DbSession):
    # ListModelクラスのインスタンスを生成する
    db_item = ListModel(title=new_todo_list.title, description=new_todo_list.description)
    # addしてcommitすることで、DBに保存
    db.add(db_item)
    db.commit()
    # DB保存によって採番されたidやcreated_atをdb_itemオブジェクトに反映
    db.refresh(db_item)
    return db_item


@router.put("/{todo_list_id}", response_model=ResponseTodoList)
def put_todo_list(todo_list_id: int, update_todo_list: UpdateTodoList, db: DbSession):
    # Station6と同様に、更新対象のレコードをDBから取得
    db_item = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
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


@router.delete("/{todo_list_id}")
def delete_todo_list(todo_list_id: int, db: DbSession):
    # Station6と同様に、削除対象のレコードをDBから取得
    db_item = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    # レコードを削除してDBに反映
    db.delete(db_item)
    db.commit()
    # 削除系は空のJSONを返す（明示的にreturnしないとnullになる）
    return {}
