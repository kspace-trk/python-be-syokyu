from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_todo_list_404_list_not_found():
    """Station16合格判定テストコード."""
    # テスト実行
    response = client.get("/lists/-1")

    # 実行結果の検証
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_todo_list_422_title_validation_error() -> None:
    """Station16合格判定テストコード."""
    # テスト実行
    response = client.post("/lists", json={
        "title": "",
        "description": "This todo was made by the test of Station16.",
    })

    # 実行結果の検証
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_put_todo_list_404_list_not_found() -> None:
    """Station16合格判定テストコード."""
    # テスト実行
    response = client.put("/lists/-1", json={
        "title": "test_todo_station_16",
        "description": "This todo was modified by the test of Station16.",
    })

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_todo_list_404_list_not_found() -> None:
    """Station16合格判定テストコード."""
    # テスト実行
    response = client.delete("/lists/-1")

    assert response.status_code == status.HTTP_404_NOT_FOUND
