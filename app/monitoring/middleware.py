import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/metrics":
            return await call_next(request)
        
        REQUEST_COUNT.inc()
        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time
        REQUEST_LATENCY.observe(duration)
        return response
