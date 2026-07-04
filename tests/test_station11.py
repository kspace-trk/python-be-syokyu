from fastapi import status
from fastapi.testclient import TestClient

from app.const import TodoItemStatusCode
from app.main import app
from app.models import item_model, list_model
from tests.conftest import refresh_session

client = TestClient(app)


def test_post_todo_item(db_session) -> None:
    """Station11合格判定テストコード."""
    # ******************
    # 事前準備
    # ******************
    # テスト用にTODOリストをインサート
    db_todo_list = list_model.ListModel(title="station11_test", description="A test record for station11.")
    db_session.add(db_todo_list)
    db_session.commit()
    db_session.refresh(db_todo_list)

    # ******************
    # テスト実行
    # ******************
    target_todo_list_id = db_todo_list.id
    response = client.post(f"/lists/{target_todo_list_id}/items", json={
        "title": "station11_test",
        "description": "A test record for station11.",
        "due_at": "2024-09-08T12:47:23",
    })

    # ******************
    # 実行結果の検証開始
    # ******************
    # 検証に支障を来たす不要なトランザクション破棄のためDBセッションのリセット
    refresh_session(db_session)

    # ステータスコードの確認
    assert response.status_code == status.HTTP_200_OK

    # レスポンスBodyの確認
    response_body = response.json()
    db_todo_item = db_session.query(item_model.ItemModel).filter(item_model.ItemModel.id == response_body["id"]).first()
    assert response_body["todo_list_id"] == target_todo_list_id
    assert response_body["title"] == "station11_test"
    assert response_body["description"] == "A test record for station11."
    assert response_body["status_code"] == TodoItemStatusCode.NOT_COMPLETED.value
    assert response_body["due_at"] == db_todo_item.due_at.strftime("%Y-%m-%dT%H:%M:%S")
    assert response_body["created_at"] == db_todo_item.created_at.strftime("%Y-%m-%dT%H:%M:%S")
    assert response_body["updated_at"] == db_todo_item.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
