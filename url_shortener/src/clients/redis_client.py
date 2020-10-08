import typing as t

import aioredis
from aioredis import ConnectionsPool

from url_shortener.src.exceptions import NotInitException


class RedisClient:
    def __init__(self, redis_dsn: str):
        self.__redis_dsn = redis_dsn
        self.__redis_pool: t.Optional[ConnectionsPool] = None

    async def async_init(self):
        self.__redis_pool = await aioredis.create_redis_pool(self.__redis_dsn)

    async def async_stop(self):
        redis = self.__redis_pool
        if not redis:
            raise Exception("Stopped before init. Nothing to stop")

        redis.close()
        await redis.wait_closed()

        self.__redis_pool = None

    def _check_redis(self):
        if not self.__redis_pool:
            raise NotInitException()

    async def set_dict_with_ttl(
        self, key: str, url_dict: t.Dict[str, t.Any], ttl_ms: int
    ) -> bool:
        self._check_redis()

        redis = self.__redis_pool

        await redis.hmset_dict(key, url_dict)
        await redis.expire(key, ttl_ms)

        return True

    async def get_dict(self, key: str) -> t.Dict[str, t.Any]:
        self._check_redis()

        redis = self.__redis_pool

        return await redis.hgetall(key, encoding="utf-8")
