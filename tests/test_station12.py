import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.const import TodoItemStatusCode
from app.main import app
from app.models import item_model, list_model
from tests.conftest import refresh_session

client = TestClient(app)


@pytest.mark.parametrize("status_code", [
    (TodoItemStatusCode.COMPLETED.value),
    (TodoItemStatusCode.NOT_COMPLETED.value),
])
def test_put_todo_item(status_code: int, db_session) -> None:
    """Station12合格判定テストコード."""
    # ******************
    # 事前準備
    # ******************
    # テスト用にTODOリストをインサート
    db_todo_list = list_model.ListModel(title="station12_test", description="A test record for station12.")
    db_session.add(db_todo_list)
    db_session.commit()
    db_session.refresh(db_todo_list)

    # テスト用にTODO項目をインサート
    db_todo_item = item_model.ItemModel(
        todo_list_id=db_todo_list.id,
        title="station12_test",
        description="A test record for station12.",
        status_code=1,
    )
    db_session.add(db_todo_item)
    db_session.commit()

    # ******************
    # テスト実行
    # ******************
    target_todo_list_id = db_todo_list.id
    target_todo_item_id = db_todo_item.id
    response = client.put(
        f"/lists/{target_todo_list_id}/items/{target_todo_item_id}",
        json={
            "title": "updated_station12_test",
            "description": "An updated test record for station12.",
            "due_at": "2024-09-08T12:54:53",
            "complete": status_code == TodoItemStatusCode.COMPLETED.value,
        },
    )

    # ******************
    # 実行結果の検証開始
    # ******************
    # 検証に支障を来たす不要なトランザクション破棄のためDBセッションのリセット
    refresh_session(db_session)

    # ステータスコードの確認
    assert response.status_code == status.HTTP_200_OK

    # レスポンスBodyの確認
    response_body = response.json()
    db_todo_item = db_session.query(item_model.ItemModel).filter(item_model.ItemModel.id == target_todo_item_id).first()
    assert response_body["id"] == target_todo_item_id
    assert response_body["todo_list_id"] == target_todo_list_id
    assert response_body["title"] == "updated_station12_test"
    assert response_body["description"] == "An updated test record for station12."
    assert response_body["status_code"] == status_code
    assert response_body["due_at"] == "2024-09-08T12:54:53"
    assert response_body["created_at"] == db_todo_item.created_at.strftime("%Y-%m-%dT%H:%M:%S")
    assert response_body["updated_at"] == db_todo_item.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
