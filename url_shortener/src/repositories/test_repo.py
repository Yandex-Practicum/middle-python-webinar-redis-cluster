from unittest.mock import AsyncMock

import pytest

from url_shortener.src.clients.redis_client import RedisClient
from url_shortener.src.models import Url
from url_shortener.src.repositories import UrlRepository


@pytest.fixture()
def mock_redis_client(monkeypatch):
    m = AsyncMock(return_value={})

    monkeypatch.setattr(RedisClient, "async_init", m)
    monkeypatch.setattr(RedisClient, "_check_redis", lambda _: True)
    monkeypatch.setattr(RedisClient, "get_dict", m)
    monkeypatch.setattr(RedisClient, "set_dict_with_ttl", m)

    return RedisClient("")


@pytest.mark.asyncio
async def test_create_url__hp(mock_redis_client):
    repo = UrlRepository(
        _redis_client=mock_redis_client, _main_url="http://test_main_url.url"
    )
    await repo.async_init()
    result = await repo.create_url("http://testurl.url", 6, 100)
    assert repo.calculate_url_key("http://testurl.url", 6) == "ZWKRjN"
    assert result == Url(
        full_path="http://testurl.url",
        redirect_path="http://test_main_url.url:8000/short_url/r/ZWKRjN",
        url_key="ZWKRjN",
    )
