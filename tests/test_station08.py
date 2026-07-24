from datetime import datetime

from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.models import list_model
from tests.conftest import refresh_session

client = TestClient(app)


def test_put_todo_list(db_session) -> None:
    """Station08合格判定テストコード."""
    db_item = list_model.ListModel(title="station08_test", description="A test record for station08.")

    # テスト用にインサート
    db_session.add(db_item)
    db_session.commit()
    db_session.refresh(db_item)

    # テスト実行
    response = client.put(f"/lists/{db_item.id}", json={
        "title": "test_todo_station_08",
        "description": "This todo was modified by the test of Station08.",
    })

    # 実行結果の検証
    refresh_session(db_session)

    assert response.status_code == status.HTTP_200_OK

    response_body = response.json()
    assert response_body["id"] == db_item.id

    updated_db_item = db_session.query(list_model.ListModel).filter(list_model.ListModel.id == response_body["id"]).first()

    if updated_db_item is None:
        msg = "PUTしたデータがレスポンス情報に基づいて取得できませんでした。"
        raise AssertionError(msg)

    assert response_body["title"] == "test_todo_station_08"
    assert response_body["title"] == updated_db_item.title
    assert response_body["description"] == "This todo was modified by the test of Station08."
    assert response_body["description"] == updated_db_item.description

    assert datetime.strptime(response_body["created_at"], "%Y-%m-%dT%H:%M:%S") == updated_db_item.created_at  # noqa: DTZ007
    assert datetime.strptime(response_body["updated_at"], "%Y-%m-%dT%H:%M:%S") == updated_db_item.updated_at  # noqa: DTZ007
