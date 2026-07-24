from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.models import list_model
from tests.conftest import refresh_session

client = TestClient(app)


def test_delete_todo_list(db_session) -> None:
    """Station09合格判定テストコード."""
    db_item = list_model.ListModel(title="station09_test", description="A test record for station09.")

    # テスト用にインサート
    db_session.add(db_item)
    db_session.commit()

    # テスト実行
    target_todo_list_id = db_item.id
    response = client.delete(f"/lists/{target_todo_list_id}")

    # 実行結果の検証
    refresh_session(db_session)

    assert response.status_code == status.HTTP_200_OK

    # レスポンスBodyの確認
    response_body = response.json()
    assert response_body == {}

    # 削除されているかの確認
    db_item = db_session.query(list_model.ListModel).filter(list_model.ListModel.id == target_todo_list_id).first()
    assert db_item is None
