"""TODO項目のAPI."""

from fastapi import APIRouter

from app.crud import item_crud
from app.dependencies import DbSession
from app.schemas.item_schema import NewTodoItem, ResponseTodoItem, UpdateTodoItem

# prefixにはパスパラメータを含められる。todo_list_idは各関数の引数で受け取る
router = APIRouter(
    prefix="/lists/{todo_list_id}/items",
    tags=["Todo項目"],
)


# 固定パスは、パスパラメータを含むパスより先に定義する
@router.get("/", response_model=list[ResponseTodoItem])
def get_todo_items(todo_list_id: int, db: DbSession):
    return item_crud.get_todo_items(db, todo_list_id)


@router.get("/{todo_item_id}", response_model=ResponseTodoItem)
def get_todo_item(todo_list_id: int, todo_item_id: int, db: DbSession):
    return item_crud.get_todo_item(db, todo_list_id, todo_item_id)


@router.post("/", response_model=ResponseTodoItem)
def post_todo_item(todo_list_id: int, new_todo_item: NewTodoItem, db: DbSession):
    return item_crud.create_todo_item(db, todo_list_id, new_todo_item)


@router.put("/{todo_item_id}", response_model=ResponseTodoItem)
def put_todo_item(todo_list_id: int, todo_item_id: int, update_todo_item: UpdateTodoItem, db: DbSession):
    return item_crud.update_todo_item(db, todo_list_id, todo_item_id, update_todo_item)


@router.delete("/{todo_item_id}")
def delete_todo_item(todo_list_id: int, todo_item_id: int, db: DbSession):
    item_crud.delete_todo_item(db, todo_list_id, todo_item_id)
    # 削除系は空のJSONを返す（明示的にreturnしないとnullになる）
    return {}
