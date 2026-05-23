import pytest
from redis_om import NotFoundError
from unittest.mock import MagicMock
from payment.main import Order

def test_order_model_integration_with_redis_error(mocker):
    mock_get = mocker.patch.object(Order, "get")
    
    mock_get.side_effect = NotFoundError()

    with pytest.raises(NotFoundError):
        Order.get("nepostojeci_id")