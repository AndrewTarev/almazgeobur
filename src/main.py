from contextlib import asynccontextmanager
from typing import AsyncIterator

import redis
import uvicorn
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api.v1 import router
from src.core.config import settings
from src.core.db_helper import db_helper
from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis_cache = redis.from_url(settings.cache_url.redis_cache)
    FastAPICache.init(RedisBackend(redis_cache), prefix="fastapi-cache")
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "result": False,
            "error_type": exc.status_code,
            "error_message": exc.detail,
        },
    )


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
