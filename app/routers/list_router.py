"""TODOリストのAPI."""

from fastapi import APIRouter

from app.dependencies import DbSession
from app.models.list_model import ListModel
from app.schemas.list_schema import ResponseTodoList

# prefixでパスの共通部分を、tagsでSwagger UI上のグループをまとめて指定する
router = APIRouter(
    prefix="/lists",
    tags=["Todoリスト"],
)


# prefixが付くため、デコレータには/lists以降だけを書く
@router.get("/{todo_list_id}", response_model=ResponseTodoList)
def get_todo_list(todo_list_id: int, db: DbSession):
    query = db.query(ListModel).filter(ListModel.id == todo_list_id)
    print(query)
    db_item = query.first()
    return db_item
