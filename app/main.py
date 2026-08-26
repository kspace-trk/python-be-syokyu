import os

from fastapi import FastAPI

from app.const import TodoItemStatusCode
from app.schemas.item_schema import NewTodoItem, ResponseTodoItem, UpdateTodoItem
from app.schemas.list_schema import NewTodoList, ResponseTodoList, UpdateTodoList

from .models.item_model import ItemModel
from .models.list_model import ListModel

from app.dependencies import DbSession
from app.routers import item_router, list_router

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

# 各モジュールに分割したルーターをアプリケーションへ合流させる
app.include_router(list_router.router)
app.include_router(item_router.router)


@app.get("/echo", tags=["Echo"])
def get_echo(message: str, name: str):
    return {"Message": f"{message} {name}!"}


@app.get("/health", tags=["System"])
def get_health():
    return {"status": "ok"}
