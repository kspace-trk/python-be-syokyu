import os
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

from app.const import TodoItemStatusCode

from .models.item_model import ItemModel
from .models.list_model import ListModel

from app.dependencies import DbSession

DEBUG = os.environ.get("DEBUG", "") == "true"

app = FastAPI(
    title="Python Backend Stations",
    debug=DEBUG,
)

if DEBUG:
    from debug_toolbar.middleware import DebugToolbarMiddleware

    # panelsに追加で表示するパネルを指定できる
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["app.database.SQLAlchemyPanel"],
    )


class NewTodoItem(BaseModel):
    """TODO項目新規作成時のスキーマ."""

    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    due_at: datetime | None = Field(default=None, title="Todo Item Due")


class UpdateTodoItem(BaseModel):
    """TODO項目更新時のスキーマ."""

    title: str | None = Field(default=None, title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    complete: bool | None = Field(default=None, title="Set Todo Item status as completed")


class ResponseTodoItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    todo_list_id: int
    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    status_code: TodoItemStatusCode = Field(title="Todo Status Code")
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")


class NewTodoList(BaseModel):
    """TODOリスト新規作成時のスキーマ."""

    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)


class UpdateTodoList(BaseModel):
    """TODOリスト更新時のスキーマ."""

    title: str | None = Field(default=None, title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)


class ResponseTodoList(BaseModel):
    """TODOリストのレスポンススキーマ."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")

@app.get("/echo", tags=["Echo"])
def get_echo(message: str, name: str):
    return {"Message": f"{message} {name}!"}

@app.get("/health", tags=["System"])
def get_health():
    return {"status": "ok"}

@app.get("/lists/{todo_list_id}", tags=["Todoリスト"], response_model=ResponseTodoList)
def get_todo_list(todo_list_id: int, db: DbSession):
    query = db.query(ListModel).filter(ListModel.id == todo_list_id)
    print(query)
    db_item = query.first()
    return db_item


@app.post("/lists", tags=["Todoリスト"], response_model=ResponseTodoList)
def post_todo_list(new_todo_list: NewTodoList, db: DbSession):
    # ListModelクラスのインスタンスを生成する
    db_item = ListModel(title=new_todo_list.title, description=new_todo_list.description)
    # addしてcommitすることで、DBに保存
    db.add(db_item)
    db.commit()
    # DB保存によって採番されたidやcreated_atをdb_itemオブジェクトに反映
    db.refresh(db_item)
    return db_item


@app.put("/lists/{todo_list_id}", tags=["Todoリスト"], response_model=ResponseTodoList)
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


@app.delete("/lists/{todo_list_id}", tags=["Todoリスト"])
def delete_todo_list(todo_list_id: int, db: DbSession):
    # Station6と同様に、削除対象のレコードをDBから取得
    db_item = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    # レコードを削除してDBに反映
    db.delete(db_item)
    db.commit()
    # 削除系は空のJSONを返す（明示的にreturnしないとnullになる）
    return {}


@app.get("/lists/{todo_list_id}/items/{todo_item_id}", tags=["Todo項目"], response_model=ResponseTodoItem)
def get_todo_item(todo_list_id: int, todo_item_id: int, db: DbSession):
    db_item = db.query(ItemModel).filter(ItemModel.id == todo_item_id,ItemModel.todo_list_id == todo_list_id,).first()
    return db_item


@app.post("/lists/{todo_list_id}/items", tags=["Todo項目"], response_model=ResponseTodoItem)
def post_todo_item(todo_list_id: int, new_todo_item: NewTodoItem, db: DbSession):
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


@app.put("/lists/{todo_list_id}/items/{todo_item_id}", tags=["Todo項目"], response_model=ResponseTodoItem)
def put_todo_item(todo_list_id: int, todo_item_id: int, update_todo_item: UpdateTodoItem, db: DbSession):
    # Station10と同様に、todo_list_idとtodo_item_idの両方で絞り込んで更新対象を取得
    db_item = db.query(ItemModel).filter(ItemModel.id == todo_item_id, ItemModel.todo_list_id == todo_list_id).first()
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


@app.delete("/lists/{todo_list_id}/items/{todo_item_id}", tags=["Todo項目"])
def delete_todo_item(todo_list_id: int, todo_item_id: int, db: DbSession):
    # Station10と同様に、todo_list_idとtodo_item_idの両方で絞り込んで削除対象を取得
    db_item = db.query(ItemModel).filter(ItemModel.id == todo_item_id, ItemModel.todo_list_id == todo_list_id).first()
    # レコードを削除してDBに反映
    db.delete(db_item)
    db.commit()
    # 削除系は空のJSONを返す（明示的にreturnしないとnullになる）
    return {}
