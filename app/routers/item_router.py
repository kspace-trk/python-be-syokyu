"""TODO項目のAPI."""

from fastapi import APIRouter, HTTPException, status

from app.crud import item_crud, list_crud
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
    db_item = item_crud.get_todo_item(db, todo_list_id, todo_item_id)
    # 両方のIDで絞り込んでいるので、リストと項目どちらが無くてもNoneになる
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")
    return db_item


@router.post("/", response_model=ResponseTodoItem)
def post_todo_item(todo_list_id: int, new_todo_item: NewTodoItem, db: DbSession):
    # 作成時はまだ項目が無いので、親のTODOリストの存在だけを単独で確認する
    # （確認せずに登録すると外部キー制約違反で500になる）
    db_item = list_crud.get_todo_list(db, todo_list_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo list not found")
    return item_crud.create_todo_item(db, todo_list_id, new_todo_item)


@router.put("/{todo_item_id}", response_model=ResponseTodoItem)
def put_todo_item(todo_list_id: int, todo_item_id: int, update_todo_item: UpdateTodoItem, db: DbSession):
    db_item = item_crud.update_todo_item(db, todo_list_id, todo_item_id, update_todo_item)
    # 更新対象が無ければ404を返す
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")
    return db_item


@router.delete("/{todo_item_id}")
def delete_todo_item(todo_list_id: int, todo_item_id: int, db: DbSession):
    # crud側は削除できたか否かを返すので、その結果で404を判定する
    result = item_crud.delete_todo_item(db, todo_list_id, todo_item_id)
    if result == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")
    # 削除系は空のJSONを返す（明示的にreturnしないとnullになる）
    return {}
