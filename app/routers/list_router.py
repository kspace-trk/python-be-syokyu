"""TODOリストのAPI."""

from fastapi import APIRouter, HTTPException, status

from app.crud import list_crud
from app.dependencies import DbSession
from app.schemas.list_schema import NewTodoList, ResponseTodoList, UpdateTodoList

# prefixでパスの共通部分を、tagsでSwagger UI上のグループをまとめて指定する
router = APIRouter(
    prefix="/lists",
    tags=["Todoリスト"],
)


# 固定パスは、パスパラメータを含むパスより先に定義する
@router.get("/", response_model=list[ResponseTodoList])
def get_todo_lists(db: DbSession):
    return list_crud.get_todo_lists(db)


@router.get("/{todo_list_id}", response_model=ResponseTodoList)
def get_todo_list(todo_list_id: int, db: DbSession):
    db_item = list_crud.get_todo_list(db, todo_list_id)
    # 該当データが無ければ404を返す
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo list not found")
    return db_item


@router.post("/", response_model=ResponseTodoList)
def post_todo_list(new_todo_list: NewTodoList, db: DbSession):
    return list_crud.create_todo_list(db, new_todo_list)


@router.put("/{todo_list_id}", response_model=ResponseTodoList)
def put_todo_list(todo_list_id: int, update_todo_list: UpdateTodoList, db: DbSession):
    db_item = list_crud.update_todo_list(db, todo_list_id, update_todo_list)
    # 更新対象が無ければ404を返す
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo list not found")
    return db_item


@router.delete("/{todo_list_id}")
def delete_todo_list(todo_list_id: int, db: DbSession):
    # crud側は削除できたか否かを返すので、その結果で404を判定する
    if not list_crud.delete_todo_list(db, todo_list_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo list not found")
    # 削除系は空のJSONを返す（明示的にreturnしないとnullになる）
    return {}
