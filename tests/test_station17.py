from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.models import item_model, list_model

client = TestClient(app)


def test_get_todo_item_404_list_not_found(db_session) -> None:
    """Station17合格判定テストコード."""
    # ******************
    # 事前準備
    # ******************
    # テスト用にTODOリストをインサート
    db_todo_list = list_model.ListModel(title="station17_test", description="A test record for station17.")
    db_session.add(db_todo_list)
    db_session.commit()
    db_session.refresh(db_todo_list)

    # テスト用にTODO項目をインサート
    db_todo_item = item_model.ItemModel(
        todo_list_id=db_todo_list.id,
        title="station17_test",
        description="A test record for station17.",
        status_code=1,
    )
    db_session.add(db_todo_item)
    db_session.commit()

    target_todo_item_id = db_todo_item.id

    # ******************
    # テスト実行_01
    # ******************
    response = client.get(f"/lists/-1/items/{target_todo_item_id}")

    # ******************
    # 実行結果の検証開始_01
    # ******************
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_todo_item_404_item_not_found(db_session) -> None:
    """Station17合格判定テストコード."""
    # ******************
    # 事前準備
    # ******************
    # テスト用にTODOリストをインサート
    db_todo_list = list_model.ListModel(title="station17_test", description="A test record for station17.")
    db_session.add(db_todo_list)
    db_session.commit()
    db_session.refresh(db_todo_list)

    target_todo_list_id = db_todo_list.id

    # ******************
    # テスト実行_02
    # ******************
    target_todo_list_id = db_todo_list.id
    response = client.get(f"/lists/{target_todo_list_id}/items/-1")

    # ******************
    # 実行結果の検証開始_02
    # ******************
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_todo_item_404_list_not_found() -> None:
    """Station17合格判定テストコード."""
    # ******************
    # テスト実行
    # ******************
    response = client.post("/lists/-1/items", json={
        "title": "station17_test",
        "description": "A test record for station17.",
        "due_at": "2024-09-08T16:47:23",
    })

    # ******************
    # 実行結果の検証開始
    # ******************

    # ステータスコードの確認
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_todo_item_422_validation_error(db_session) -> None:
    """Station17合格判定テストコード."""
    # ******************
    # 事前準備
    # ******************
    # テスト用にTODOリストをインサート
    db_todo_list = list_model.ListModel(title="station17_test", description="A test record for station17.")
    db_session.add(db_todo_list)
    db_session.commit()
    db_session.refresh(db_todo_list)

    # ******************
    # テスト実行
    # ******************
    target_todo_list_id = db_todo_list.id
    response = client.post(f"/lists/{target_todo_list_id}/items", json={
        "title": "",
        "description": "A test record for station17.",
        "due_at": "2024-09-08T16:47:23",
    })

    # ******************
    # 実行結果の検証開始
    # ******************
    # ステータスコードの確認
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_put_todo_item_404_list_not_found(db_session) -> None:
    """Station17合格判定テストコード."""
    # ******************
    # 事前準備
    # ******************
    # テスト用にTODOリストをインサート
    db_todo_list = list_model.ListModel(title="station17_test", description="A test record for station17.")
    db_session.add(db_todo_list)
    db_session.commit()
    db_session.refresh(db_todo_list)

    # テスト用にTODO項目をインサート
    db_todo_item = item_model.ItemModel(
        todo_list_id=db_todo_list.id,
        title="station17_test",
        description="A test record for station17.",
        status_code=1,
    )
    db_session.add(db_todo_item)
    db_session.commit()
    db_session.refresh(db_todo_item)

    target_todo_item_id = db_todo_item.id

    # ******************
    # テスト実行
    # ******************
    response = client.put(
        f"/lists/-1/items/{target_todo_item_id}",
        json={
            "title": "updated_station17_test",
            "description": "An updated test record for station17.",
            "due_at": "2024-09-08T16:54:53",
            "complete": True,
        },
    )

    # ******************
    # 実行結果の検証開始
    # ******************
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_put_todo_item_404_item_not_found(db_session) -> None:
    """Station17合格判定テストコード."""
    # ******************
    # 事前準備
    # ******************
    # テスト用にTODOリストをインサート
    db_todo_list = list_model.ListModel(title="station17_test", description="A test record for station17.")
    db_session.add(db_todo_list)
    db_session.commit()
    db_session.refresh(db_todo_list)

    target_todo_list_id = db_todo_list.id

    # ******************
    # テスト実行
    # ******************
    response = client.put(
        f"/lists/{target_todo_list_id}/items/-1",
        json={
            "title": "updated_station17_test",
            "description": "An updated test record for station17.",
            "due_at": "2024-09-08T16:54:53",
            "complete": True,
        },
    )

    # ******************
    # 実行結果の検証開始
    # ******************
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_todo_item_404_list_not_found(db_session) -> None:
    """Station17合格判定テストコード."""
    # ******************
    # 事前準備
    # ******************
    # テスト用にTODOリストをインサート
    db_todo_list = list_model.ListModel(title="station17_test", description="A test record for station17.")
    db_session.add(db_todo_list)
    db_session.commit()
    db_session.refresh(db_todo_list)

    # テスト用にTODO項目をインサート
    db_todo_item = item_model.ItemModel(
        todo_list_id=db_todo_list.id,
        title="station17_test",
        description="A test record for station17.",
        status_code=1,
    )
    db_session.add(db_todo_item)
    db_session.commit()

    # ******************
    # テスト実行
    # ******************
    target_todo_item_id = db_todo_item.id
    response = client.delete(f"/lists/-1/items/{target_todo_item_id}")

    # ******************
    # 実行結果の検証開始
    # ******************
    # ステータスコードの確認
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_todo_item(db_session) -> None:
    """Station17合格判定テストコード."""
    # ******************
    # 事前準備
    # ******************
    # テスト用にTODOリストをインサート
    db_todo_list = list_model.ListModel(title="station17_test", description="A test record for station17.")
    db_session.add(db_todo_list)
    db_session.commit()
    db_session.refresh(db_todo_list)

    # ******************
    # テスト実行
    # ******************
    target_todo_list_id = db_todo_list.id
    response = client.delete(f"/lists/{target_todo_list_id}/items/-1")

    # ******************
    # 実行結果の検証開始
    # ******************
    # ステータスコードの確認
    assert response.status_code == status.HTTP_404_NOT_FOUND
