import pytest
from unittest.mock import AsyncMock, MagicMock
from payment.main import process_order, Order

@pytest.mark.asyncio
async def test_process_order_logic(mocker):
    mocker.patch("asyncio.sleep", return_value=None)
    
    mock_redis = mocker.patch("payment.main.redis")
    mock_redis.xadd = MagicMock()
    mock_order = MagicMock(spec=Order)
    mock_order.status = "pending"
    mock_order.save = MagicMock()
    mock_order.model_dump.return_value = {"product_id": "123", "status": "completed"}

    await process_order(mock_order)

    assert mock_order.status == "completed"  
    mock_order.save.assert_called_once()     
    mock_redis.xadd.assert_called_once()    