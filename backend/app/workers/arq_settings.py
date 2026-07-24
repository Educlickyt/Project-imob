from arq.connections import RedisSettings
from app.core.config import settings


async def startup(ctx):
    pass


async def shutdown(ctx):
    pass


class WorkerSettings:
    functions: list = []
    redis_settings = RedisSettings(
        host=settings.REDIS_HOST,
        port=int(settings.REDIS_PORT),
    )
    on_startup = startup
    on_shutdown = shutdown
    keep_result = 3600
    max_tries = 3
    job_timeout = 300
