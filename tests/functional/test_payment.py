import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from payment.main import app, Order

client = TestClient(app)

def test_get_order_404_functional():
    with patch.object(Order, "get", side_effect=Exception("NotFoundError")):
        response = client.get("/orders/lazni-id-123")
        assert response.status_code == 404


def test_create_order_api_flow(mocker):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "prod_1", "price": 100.0}
    
    mock_async_client = mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    mocker.patch.object(Order, "save", return_value=None)
    mocker.patch("fastapi.BackgroundTasks.add_task", return_value=None)

    payload = {"id": "prod_1", "quantity": 2}
    response = client.post("/orders", json=payload)

    assert response.status_code == 200
    data = response.json()
    
    assert data["product_id"] == "prod_1"
    assert data["price"] == 100.0
    assert data["fee"] == 20.0       
    assert data["total"] == 240.0   
    assert data["status"] == "pending"