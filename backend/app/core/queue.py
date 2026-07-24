from arq import create_pool
from arq.connections import RedisSettings

from app.core.config import settings

_pool = None


async def get_queue():
    global _pool
    if _pool is None:
        _pool = await create_pool(
            RedisSettings(
                host=settings.REDIS_HOST,
                port=int(settings.REDIS_PORT),
            )
        )
    return _pool


async def enqueue_job(name: str, *args, **kwargs):
    q = await get_queue()
    return await q.enqueue_job(name, *args, **kwargs)
