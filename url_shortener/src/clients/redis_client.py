import asyncio
import typing as t

import uvloop
import aioredis
from aioredis import ConnectionsPool

from url_shortener.src.exceptions import NotInitException

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

class RedisClient:
    def __init__(self, redis_dsns: t.List[str], default_host_num: t.Optional[int] = None):
        self.__redis_dsns = redis_dsns
        self.__redis_pool: t.Optional[t.List[ConnectionsPool]] = None
        self.default_host_num = default_host_num

    async def async_init(self):
        create_redises_pools = [
            await aioredis.create_redis_pool(r_dsn)
            for r_dsn in self.__redis_dsns
        ]
        self.__redis_pool = create_redises_pools

    async def async_stop(self):
        self._check_init()

        for redis in self.__redis_pool:
            redis.close()
            await redis.wait_closed()

        self.__redis_pool = None

    def _check_init(self):
        if not self.__redis_pool:
            raise NotInitException()

    def get_redis_pool_by_key(self, key: str) -> ConnectionsPool:
        redis_num = int.from_bytes(key.encode(), byteorder="big") % len(self.__redis_pool)
        redis = self.__redis_pool[redis_num]

        return redis

    async def set_dict_with_ttl(self, key: str, url_dict: dict, ttl_ms: int) -> bool:
        self._check_init()

        redis = self.get_redis_pool_by_key(key)

        await redis.hmset_dict(key, url_dict)
        await redis.expire(key, ttl_ms)

        return True

    async def get_dict(self, key: str) -> t.Dict[str, t.Any]:
        self._check_init()

        redis = self.get_redis_pool_by_key(key)

        result = await redis.hgetall(key, encoding="utf-8")
        if not result and self.default_host_num is not None:
            redis = self.__redis_pool[self.default_host_num]
            result = await redis.hgetall(key, encoding="utf-8")

        return result
