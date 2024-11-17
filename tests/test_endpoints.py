import pytest
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from httpx import AsyncClient

from src.main import app


@pytest.mark.asyncio
async def test_contact_us(ac: AsyncClient) -> None:
    with patch("httpx.AsyncClient") as mock_client:
        mock_post = AsyncMock()
        mock_client.return_value.__aenter__.return_value.post = mock_post

        response = await ac.post(
            url="/api/v1/parse-xml/",
            json={
                "desc": "desc",
                "name": "Brid Pett",
                "phone": "123456789",
                "email": "test@cc.cc",
            },
        )
        mock_post.assert_called_once()
        assert response.status_code == 200
