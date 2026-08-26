import os

from fastapi import FastAPI

from app.const import TodoItemStatusCode
from app.routers import list_router
from app.schemas.item_schema import NewTodoItem, ResponseTodoItem, UpdateTodoItem
from app.schemas.list_schema import NewTodoList, ResponseTodoList, UpdateTodoList

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

# 別モジュールに分割したルーターをアプリケーションへ合流させる
app.include_router(list_router.router)


@app.get("/echo", tags=["Echo"])
def get_echo(message: str, name: str):
    return {"Message": f"{message} {name}!"}

@app.get("/health", tags=["System"])
def get_health():
    return {"status": "ok"}


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
