"""TODOリストのAPI."""

from fastapi import APIRouter

from app.crud import list_crud
from app.dependencies import DbSession
from app.schemas.list_schema import NewTodoList, ResponseTodoList, UpdateTodoList

# prefixでパスの共通部分を、tagsでSwagger UI上のグループをまとめて指定する
router = APIRouter(
    prefix="/lists",
    tags=["Todoリスト"],
)


@router.get("/{todo_list_id}", response_model=ResponseTodoList)
def get_todo_list(todo_list_id: int, db: DbSession):
    return list_crud.get_todo_list(db, todo_list_id)


@router.post("/", response_model=ResponseTodoList)
def post_todo_list(new_todo_list: NewTodoList, db: DbSession):
    return list_crud.create_todo_list(db, new_todo_list)


@router.put("/{todo_list_id}", response_model=ResponseTodoList)
def put_todo_list(todo_list_id: int, update_todo_list: UpdateTodoList, db: DbSession):
    return list_crud.update_todo_list(db, todo_list_id, update_todo_list)


@router.delete("/{todo_list_id}")
def delete_todo_list(todo_list_id: int, db: DbSession):
    list_crud.delete_todo_list(db, todo_list_id)
    # 削除系は空のJSONを返す（明示的にreturnしないとnullになる）
    return {}
