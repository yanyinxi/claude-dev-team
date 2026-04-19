"""
请求日志中间件

每个 HTTP 请求输出一行结构化日志，包含：
- 请求 ID（UUID）
- 方法与路径
- 状态码
- 耗时（毫秒）
- 客户端 IP

配合标准 Python logging，可被 Docker/systemd 统一采集。
"""
import logging
import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("api.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())[:8]
        start = time.perf_counter()
        client = request.client.host if request.client else "-"

        try:
            response = await call_next(request)
        except Exception:
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.exception(
                "req_id=%s method=%s path=%s client=%s status=500 ms=%.1f",
                request_id, request.method, request.url.path, client, elapsed_ms,
            )
            raise

        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "req_id=%s method=%s path=%s client=%s status=%d ms=%.1f",
            request_id, request.method, request.url.path, client,
            response.status_code, elapsed_ms,
        )
        return response


def configure_logging(level: str = "INFO") -> None:
    """配置根 logger。在 main.py 启动时调用一次。"""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
