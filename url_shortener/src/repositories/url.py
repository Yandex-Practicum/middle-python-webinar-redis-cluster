import base64
import hashlib
import json

from dataclasses import dataclass

import yarl
from pydantic import HttpUrl

from .. import config
from ..clients.redis_client import RedisClient
from ..exceptions import NotInitException
from ..models import Url


@dataclass
class UrlRepository:
    _redis_client: RedisClient
    _main_url: str
    __is_initialized: bool = False

    async def async_init(self):
        await self._redis_client.async_init()
        self.__is_initialized = True

    async def async_stop(self):
        await self._redis_client.async_stop()
        self.__is_initialized = False

    async def fetch_by_key(self, key: str) -> Url:
        if not self.__is_initialized:
            raise NotInitException()

        url_dict = await self._redis_client.get_dict(key)
        url = Url(**url_dict)

        return url

    async def create_url(self, url: HttpUrl, min_length: int, ttl_s: int) -> Url:
        if not self.__is_initialized:
            raise NotInitException()

        url_key = await self._find_collision_free_key(url, min_length)
        redirect_path = str(
            yarl.URL(self._main_url).with_port(8000) / f"short_url/r/{url_key}"
        )

        url_obj = Url(full_path=url, redirect_path=redirect_path, url_key=url_key)

        url_dict = json.loads(url_obj.json())
        await self._redis_client.set_dict_with_ttl(url_key, url_dict, ttl_s)

        return url_obj

    async def _find_collision_free_key(self, url: str, min_length: int) -> str:
        cur_len = min_length
        is_collision = True
        while is_collision:
            url_key = UrlRepository.calculate_url_key(url, min_length)
            existing_url_dict = await self._redis_client.get_dict(url_key)

            is_collision = bool(existing_url_dict) and existing_url_dict["url"] != url
            cur_len += 1

        return url_key

    @staticmethod
    def calculate_url_key(url: str, length: int) -> str:
        url_hash = hashlib.sha256(url.encode())
        hash_str = base64.urlsafe_b64encode(url_hash.digest()).decode("ascii")

        return hash_str[:length]


def init_repository(redis_dsn: str, main_service_url: str):
    return UrlRepository(
        RedisClient(redis_dsn),
        main_service_url,
    )


url_repository = init_repository(str(config.REDIS_DSN), config.MAIN_SERVICE_URL)
